import os
import random
import time
from tools_and_schemas import SearchQueryList, Reflection
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.types import Send
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig
from google.genai import Client

from state import (
    OverallState,
    QueryGenerationState,
    ReflectionState,
    WebSearchState,
)
from configuration import Configuration
from prompts import (
    get_current_date,
    query_writer_instructions,
    web_searcher_instructions,
    reflection_instructions,
    answer_instructions,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import (
    get_citations,
    get_research_topic,
    insert_citation_markers,
    resolve_urls,
)

load_dotenv()

if os.getenv("GEMINI_API_KEY_1") is None:
    raise ValueError("GEMINI_API_KEY_1 is not set")
if os.getenv("GEMINI_API_KEY_2") is None:
    raise ValueError("GEMINI_API_KEY_2 is not set")
if os.getenv("GEMINI_API_KEY_3") is None:
    raise ValueError("GEMINI_API_KEY_3 is not set")

# Load all three API keys
GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

# Create a client for each key
GEMINI_CLIENTS = [Client(api_key=key) for key in GEMINI_API_KEYS if key]

GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.5-flash-preview-04-17",
    "gemini-2.5-flash-preview-05-20"
]

def try_all_clients(api_call_fn, max_retries=5, wait_seconds=15):
    """
    Try the API call with all clients asynchronously, return on first success, else retry after wait.
    api_call_fn: function that takes a client and returns the API result.
    max_retries: how many times to retry the whole pool before giving up.
    wait_seconds: how long to wait before retrying all clients.
    """
    for attempt in range(max_retries):
        last_exception = None
        clients = GEMINI_CLIENTS.copy()
        random.shuffle(clients)
        for client in clients:
            try:
                return api_call_fn(client)
            except Exception as e:
                err_str = str(e).lower()
                if (
                    "429" in err_str or
                    "503" in err_str or
                    "quota" in err_str or
                    "rate" in err_str or
                    "unavailable" in err_str or
                    "overload" in err_str
                ):
                    last_exception = e
                    continue
                else:
                    raise  # Other errors, re-raise
        if attempt < max_retries - 1:
            print(f"All Gemini clients exhausted or rate-limited. Waiting {wait_seconds} seconds before retrying...")
            time.sleep(wait_seconds)
            wait_seconds *= 2
    if last_exception:
        raise last_exception
    raise RuntimeError("No valid Gemini API clients available.")

# Nodes
def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    configurable = Configuration.from_runnable_config(config)
    if state.get("initial_search_query_count") is None:
        state["initial_search_query_count"] = configurable.number_of_initial_queries
        
    random_model = random.choice(GEMINI_MODELS)
    llm = ChatGoogleGenerativeAI(
        model=random_model, # configurable.query_generator_model,
        temperature=1.0,
        max_retries=2,
        api_key=random.choice(GEMINI_API_KEYS),
    )
    structured_llm = llm.with_structured_output(SearchQueryList)

    current_date = get_current_date()
    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    result = structured_llm.invoke(formatted_prompt)
    return {"query_list": result.query}

def continue_to_web_research(state: QueryGenerationState):
    return [
        Send("web_research", {"search_query": search_query, "id": int(idx)})
        for idx, search_query in enumerate(state["query_list"])
    ]

def web_research(state: WebSearchState, config: RunnableConfig) -> OverallState:
    configurable = Configuration.from_runnable_config(config)
    formatted_prompt = web_searcher_instructions.format(
        current_date=get_current_date(),
        research_topic=state["search_query"],
    )

    def api_call(client):
        random_model = random.choice(GEMINI_MODELS)
        return client.models.generate_content(
            model=random_model,
            contents=formatted_prompt,
            config={
                "tools": [{"google_search": {}}],
                "temperature": 0,
            },
        )
    response = try_all_clients(api_call)

    resolved_urls = resolve_urls(
        response.candidates[0].grounding_metadata.grounding_chunks, state["id"]
    )
    citations = get_citations(response, resolved_urls)
    modified_text = insert_citation_markers(response.text, citations)
    sources_gathered = [item for citation in citations for item in citation["segments"]]

    return {
        "sources_gathered": sources_gathered,
        "search_query": [state["search_query"]],
        "web_research_result": [modified_text],
    }
    
def evaluate_research(
    state: ReflectionState,
    config: RunnableConfig,
) -> OverallState:
    """LangGraph routing function that determines the next step in the research flow.

    Controls the research loop by deciding whether to continue gathering information
    or to finalize the summary based on the configured maximum number of research loops.

    Args:
        state: Current graph state containing the research loop count
        config: Configuration for the runnable, including max_research_loops setting

    Returns:
        String literal indicating the next node to visit ("web_research" or "finalize_summary")
    """
    configurable = Configuration.from_runnable_config(config)
    max_research_loops = (
        state.get("max_research_loops")
        if state.get("max_research_loops") is not None
        else configurable.max_research_loops
    )
    if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
        return "finalize_answer"
    else:
        return [
            Send(
                "web_research",
                {
                    "search_query": follow_up_query,
                    "id": state["number_of_ran_queries"] + int(idx),
                },
            )
            for idx, follow_up_query in enumerate(state["follow_up_queries"])
        ]

def reflection(state: OverallState, config: RunnableConfig) -> ReflectionState:
    configurable = Configuration.from_runnable_config(config)
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1
    # reasoning_model = state.get("reasoning_model") or configurable.reasoning_model

    current_date = get_current_date()
    formatted_prompt = reflection_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        summaries="\n\n---\n\n".join(state["web_research_result"]),
    )
    random_model = random.choice(GEMINI_MODELS)
    llm = ChatGoogleGenerativeAI(
        model=random_model, # reasoning_model,
        temperature=1.0,
        max_retries=2,
        api_key=random.choice(GEMINI_API_KEYS),
    )
    result = llm.with_structured_output(Reflection).invoke(formatted_prompt)

    return {
        "is_sufficient": result.is_sufficient,
        "knowledge_gap": result.knowledge_gap,
        "follow_up_queries": result.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state["search_query"]),
    }

def finalize_answer(state: OverallState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    reasoning_model = state.get("reasoning_model") or configurable.reasoning_model

    current_date = get_current_date()
    formatted_prompt = answer_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        summaries="\n---\n\n".join(state["web_research_result"]),
    )

    random_model = random.choice(GEMINI_MODELS)
    llm = ChatGoogleGenerativeAI(
        model= random_model, # reasoning_model
        temperature=0,
        max_retries=2,
        api_key=random.choice(GEMINI_API_KEYS),
    )
    result = llm.invoke(formatted_prompt)

    unique_sources = []
    for source in state["sources_gathered"]:
        if source["short_url"] in result.content:
            result.content = result.content.replace(
                source["short_url"], source["value"]
            )
            unique_sources.append(source)

    return {
        "messages": [AIMessage(content=result.content)],
        "sources_gathered": unique_sources,
    }

# Create our Agent Graph
builder = StateGraph(OverallState, config_schema=Configuration)

builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)

builder.add_edge(START, "generate_query")
builder.add_conditional_edges(
    "generate_query", continue_to_web_research, ["web_research"]
)
builder.add_edge("web_research", "reflection")
builder.add_conditional_edges(
    "reflection", evaluate_research, ["web_research", "finalize_answer"]
)
builder.add_edge("finalize_answer", END)

graph = builder.compile(name="search-agent")