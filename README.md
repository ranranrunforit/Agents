## Agent/Workflow Projects



**[Email Assistant with LangGraph](./ambient_agent)**

This project implements an email assistant. The agent can triage incoming emails, generate context-aware responses, learn from user feedback, and allow for human intervention before executing critical tasks. It follows a structured, multi-stage development process that starts with a basic agent architecture and progressively adds layers of evaluation, human oversight, and long-term memory. 

**Libraries:**

- `LangGraph`: Build the email assistant as a stateful graph. The agent's logic is defined as a series of nodes (functions) and edges (control flow) that operate on a persistent state object.
- `LangChain`: Interface with Large Language Models (LLMs). The chosen model is Google's `gemini-2.0-flash`.
- `LangSmith`: For testing, debugging, and evaluating the agent. It provides tools for creating datasets, running evaluations, and tracing the agent's execution paths.
- `Pytest`: To write and run evaluation tests that are logged to LangSmith.
- `Pydantic`: Define structured data schemas for the agent's tools and forcreating structured outputs from the LLM.
- `html2text`: For parsing email content.



**[Multi-Agent Web Research Assistant](./deep_research_langgraph)**

This project develops a research assistant using a multi-agent, "plan-and-execute" architecture. The system is designed to take a user's research query, break it down into a structured plan, execute web searches to gather information, and synthesize the findings into a comprehensive report. The entire workflow is orchestrated using the LangGraph framework and powered by Google's Gemini LLMs.

**Libraries:**

- `LangGraph`: Used to build and orchestrate the multi-agent system. The project leverages `StateGraph` to create stateful, cyclical workflows that manage the interactions between different agents.
- `LangChain`: To use the `LangChain` ecosystem, including `langchain-google-genai` for interfacing with Google's Gemini models.
- `Tavily`: The `TavilySearchResults` tool is integrated to provide the research agent with robust, real-time web search capabilities.
- `Pydantic` & `TypedDict`: Python's `TypedDict` is used to define the state schema (`AgentState`) that is passed between the different nodes and agents in the graph.
- `Rich`: For enhanced notebook output and visualization.



**[LangGraph Assistant_Agent](./langgraph_basic)**

This repository build, configure, and deploy LLM-powered personal/work assistants using the LangGraph framework. The project is structured into modules that progressively build upon each other, and demonstrates the power of modular, configurable, and versioned agents for real-world task management scenarios.

**Libraries:**
- `LangGraph`: Define the structure of applications as stateful graphs with nodes and edges.
- `LangChain`: `langchain-google-genai` for LLM integrations, `langchain-core` for foundational data structures like messages, and `langchain-community` for tools like `TavilySearchResults`.
- `LangSmith`: It is used to monitor application performance, manage datasets, and run experiments.
- `Tavily`: An AI-native search engine used as a tool within the agent to perform web searches.
- `Pydantic`: Used for data validation and defining structured schemas for graph states.



**[LangSmith Tracing and Evaluation](./langsmith_basic)**

This project leverages the LangSmith platform for tracing, evaluating, and managing LLM applications. It uses LangSmith's features through a Retrieval-Augmented Generation (RAG) application built with LangChain and LangGraph. The project covers a full cycle of LLM application development, from basic tracing to advanced evaluation and prompt management.

**Libraries:**
- `LangSmith`: Used for LLM observability and evaluation.
- `LangChain` & `LangGraph`: To build the underlying RAG application that is traced and evaluated. The project uses the `langchain-google-genai` integration to work with Google's Gemini models.
- `Pydantic`: For data validation and creating structured output schemas for LLM-as-judge evaluators.
- `SKLearnVectorStore`: A scikit-learn based vector store is used for the RAG application's document retrieval component.



**[Research Chat](./research_chat)**

Research Chat is an AI-powered research assistant designed to help users explore topics interactively through a chat interface. The application leverages the Gemini language model for generating insightful responses and integrates web search capabilities to provide up-to-date information.

**Libraries:**
- `Gradio`: Builds the web-based chat UI.
- `LangChain`, `LangGraph`: Orchestrate complex conversational flows and manage agent logic.
- `Google-GenAI`, `langchain-google-genai`: Accesses the Gemini language model for advanced natural language understanding and generation.
- `DuckDuckGo-Search`: Enables real-time web search to supplement AI-generated answers.
- `Requests`: Handles HTTP requests for external APIs.
- `dotenv`: Loads environment variables for configuration.
- `Pydantic`, `typing-extensions`: Provide data validation and type support.



**[Sidekick Personal Coworker](./sidekick_personal_coworker)**

This project implement an agentic assistant using LangGraph and LangChain. The assistant can autonomously complete tasks, use external tools (like web browsing and Python code execution), and iteratively improve its work based on evaluator feedback and user-defined success criteria.

- **`sidekick.py`** defines the agent's workflow, state management, and evaluation logic. It builds a stateful graph with nodes for working, tool usage, and evaluation, allowing the assistant to loop until the task is complete or more user input is needed.
- **`sidekick_tools.py`** provides tool definitions (such as Playwright-based web browsing and other custom tools) that the agent can invoke during its workflow.

**Libraries:**
- `langgraph`: For building stateful agent graphs (`StateGraph`, `ToolNode`, etc.).
- `langchain_openai`: For LLM access (`ChatOpenAI`) and tool binding.
- `langchain_core.messages`: For structured message handling (`SystemMessage`, `HumanMessage`, `AIMessage`).
- `playwright_tools`, `other_tools`: Custom tool definitions for agent actions.
- `asyncio`, `uuid`, `datetime`: For async operations, unique IDs, and time-stamping.



**[Deep Research (OpenAI Agents SDK)](./deep_research)**

This project demonstrates a Research Agent workflow using the OpenAI Agents SDK. The agent automates the process of planning, executing, and synthesizing web research, then delivers the results via email.

- Uses a `PlannerAgent` (based on the `Agent` class) to generate relevant search queries for a given research topic.  
- Employs the `WebSearchTool` to perform web searches for each planned query.
- A `WriterAgent` creates a detailed markdown report from the search results.
- Integrates SendGrid via the `send_email` function (decorated with `@function_tool`) to send the final report as a formatted HTML email.

**Libraries:**
- `OpenAI Agents SDK`: `Agent`, `WebSearchTool`, `Runner`, `trace`, `function_tool`
- `SendGrid`: For sending emails (`sendgrid.SendGridAPIClient`, `Mail`, `Email`, `To`, `Content`)
- `Asyncio`: For asynchronous execution of search and report tasks



**[Career Conversation with Rerun](./career_conversation_with_rerun)**

This project implements a professional chatbot web application using Gradio, OpenAI, and Pushover APIs. The chatbot represents AI representative and answers questions about his career, background, and experience. It loads profile and summary data from local files and uses a LLM model for conversation. The app supports function calling for two tools: recording user contact details and logging unanswered questions. Push notifications are sent via the Pushover API when these tools are triggered.

**Libraries:**
- `gradio` (`gr.ChatInterface`): Builds the interactive web chat UI.
- `openai` (`OpenAI`): Handles LLM chat completions and function calling.
- `pypdf` (`PdfReader`): Reads and extracts text from PDF profile files.
- `requests`: Sends push notifications to Pushover.



**[GAIA Agent](./GAIA_agent)**

The project implements a tool-augmented AI agent for advanced question answering and reasoning. It integrates external knowledge bases, vector databases, and a suite of tools to enhance retrieval and reasoning capabilities.

- **Agent Architecture:**  Built using LangChain and LangGraph, the agent uses a state machine (`StateGraph`) to orchestrate interactions between the assistant (powered by `ChatGoogleGenerativeAI` with Gemini 2.0 Flash) and various tools.
- **Vector Database Integration:**  Utilizes Supabase as a vector store, with embeddings generated by `HuggingFaceEmbeddings` (`sentence-transformers/all-mpnet-base-v2`). Documents are stored and retrieved using similarity search via a custom PostgreSQL function (`match_documents_langchain`).
- **Tool Suite:**  Tools are defined using LangChain's `@tool` decorator, including arithmetic operations, Wikipedia search (`WikipediaLoader`), web search (`TavilySearchResults`), Arxiv search (`ArxivLoader`), and vector database lookup.

**Libraries:**
- `LangChain`: For agent and tool orchestration.
- `LangGraph`: To manage agent state and workflow.
- `HuggingFaceEmbeddings`: For embedding and similarity search.
- `Supabase`: As the vector database backend.
- `ChatGoogleGenerativeAI`: For LLM-based responses.

