import gradio as gr
import os
from typing import List, Dict, Any, AsyncGenerator
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Import all necessary components from the agent package
from graph import graph
from configuration import Configuration
from state import OverallState
from tools_and_schemas import SearchQueryList, Reflection
from prompts import get_current_date
from langchain_core.messages import HumanMessage, AIMessage
import asyncio

# Load environment variables
load_dotenv()

# Store chat history
chat_history = []

async def process_message(message: str, effort: str, model: str) -> AsyncGenerator[List[Dict], None]:
    try:
        # Add initial message to chat history
        chat_history.append({"role": "user", "content": message})
        #chat_history.append({"role": "assistant", "content": "Starting research process..."})
        yield chat_history.copy(), None  # Don't clear textbox during intermediate updates
        
        if effort == "low":
            initial_search_query_count = 1
            max_research_loops = 1
        elif effort == "medium":
            initial_search_query_count = 3
            max_research_loops = 3
        elif effort == "high":
            initial_search_query_count = 5
            max_research_loops = 10
        else:
            yield []
            return

        config = Configuration(
            query_generator_model=model,
            reflection_model=model,
            answer_model=model,
            number_of_initial_queries=initial_search_query_count,
            max_research_loops=max_research_loops
        )
        initial_state: OverallState = {
            "messages": [HumanMessage(content=message)],
            "search_query": [],
            "web_research_result": [],
            "sources_gathered": [],
            "initial_search_query_count": initial_search_query_count,
            "max_research_loops": max_research_loops,
            "research_loop_count": 0,
            "reasoning_model": model
        }
        
        # Add initial message to chat history
        #chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": "Starting research process..."})
        yield chat_history.copy(), None  # Don't clear textbox during intermediate updates
        
        
        # Process the message using astream
        final_result = None
        async for event in graph.astream(
            initial_state,
            config={"configurable": config.model_dump()}
        ):
            print("\n")
            print("\n")
            print("Received event:", event)  # Debug log
            print("\n")
            print("\n")
            # Handle different types of events
            current_activity = ""
            if "generate_query" in event:
                current_activity = f"🔍 Generating search queries: {', '.join(event['generate_query']['query_list'])}"
            elif "web_research" in event:
                sources = event["web_research"].get("sources_gathered", [])
                num_sources = len(sources)
                unique_labels = list(set(s.label for s in sources if hasattr(s, "label")))
                example_labels = ", ".join(unique_labels[:3])
                current_activity = f"🌐 Researching: Found {num_sources} sources about {example_labels or 'the topic'}"
            elif "reflection" in event:
                current_activity = (
                                    "✨ Research complete! Generating final answer..."
                                    if event["reflection"]["is_sufficient"]
                                    else "🤔 Analyzing results: Need more information about:\n" + "\n".join(f"- {q}" for q in event["reflection"]["follow_up_queries"])
                                )
            elif "finalize_answer" in event:
                current_activity = "📝 Composing final answer..."
                chat_history[-1] = {"role": "assistant", "content": current_activity}
                yield chat_history.copy(), None  # Don't clear textbox during intermediate updates
                
                # Extract the final result from the finalize_answer event
                if "messages" in event["finalize_answer"]:
                    messages = event["finalize_answer"]["messages"]
                    if messages and len(messages) > 0:
                        last_message = messages[-1]
                        if hasattr(last_message, "content"):
                            final_result = last_message.content
                            print("Final result received:", final_result)  # Debug log
                            # Format the result in markdown
                            formatted_result = final_result.replace("\n\n", "\n").replace("\n*", "\n\n*")
                            chat_history.pop()
                            chat_history.append({"role": "assistant", "content": formatted_result})
                            #chat_history[-1] = {"role": "assistant", "content": formatted_result}
                            current_activity = "\n✅ Research complete!"
                            chat_history.append({"role": "assistant", "content": current_activity})
                            yield chat_history.copy(), ""  # Return empty string to clear textbox

                            return
                            
            if current_activity:
                # Update the last assistant message with current activity
                chat_history[-1] = {"role": "assistant", "content": current_activity}
                yield chat_history.copy(), None  # Don't clear textbox during intermediate updates

        if not final_result:
            # If no final result was received, add an error message
            chat_history.append({"role": "assistant", "content": "❌ No response received from the research process."})
            yield chat_history.copy(), ""  # Return empty string to clear textbox

    except Exception as e:
        print("Error occurred:", str(e))  # Debug log
        error_message = f"❌ Error: {str(e)}"
        chat_history.append({"role": "assistant", "content": error_message})
        yield chat_history.copy(), ""  # Return empty string to clear textbox


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="blue",
        neutral_hue="slate",
        font=["Inter", "sans-serif"],
    ),
    css="""
    .gradio-container {
        background-color: #1f2937 !important;
        min-height: 100vh !important;
    }
    .input-box {
        background-color: #374151 !important;
        border: none !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        color: #f3f4f6 !important;
    }
    .input-box:focus {
        box-shadow: none !important;
    }
    .button {
        background-color: #2563eb !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem 1rem !important;
        color: white !important;
    }
    .button:hover {
        background-color: #1d4ed8 !important;
    }
    .button.secondary {
        background-color: #374151 !important;
    }
    .button.secondary:hover {
        background-color: #4b5563 !important;
    }
    .chat-message {
        background-color: #374151 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        color: #f3f4f6 !important;
    }
    .activity-timeline {
        background-color: #374151 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        color: #f3f4f6 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    /* Styles for the dropdowns */
    .gradio-dropdown {
        background-color: #374151 !important;
        border: none !important;
        border-radius: 0.5rem !important; /* Smaller border radius for dropdown */
        color: #f3f4f6 !important;
        /* Adjust padding as needed, might need to target inner elements */
    }
    .gradio-dropdown > label {
        color: #f3f4f6 !important;
        font-weight: bold !important; /* Make label bold like in the second image */
    }
    .gradio-dropdown input[type="text"] {
        background-color: #374151 !important;
        color: #f3f4f6 !important;
        border: none !important;
        box-shadow: none !important;
        /* Adjust padding as needed */
    }
    .gradio-dropdown .gr-dropdown-icon {
        color: #f3f4f6 !important; /* Style dropdown arrow */
    }
    """
) as demo:
    gr.Markdown(
        "<h1 style='text-align:center; color:#f3f4f6;'>Gemini Research Assistant</h1>",
        elem_id="title"
    )
    
    with gr.Column(elem_id="main-container"):
        # Chat history display
        chat_history_display = gr.Chatbot(
            type='messages',
            label="Chat History",
            elem_id="chat-history",
            elem_classes=["chat-message"],
            height=400
        )
        
        # Input form
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Ask a question...",
                show_label=False,
                container=False,
                elem_id="message-input",
                elem_classes=["input-box"],
                scale=4
            )
        
        with gr.Row():
            effort = gr.Dropdown(
                choices=["low", "medium", "high"],
                value="low",
                label="Effort",
                elem_id="effort-select",
                scale=1
            )
            model = gr.Dropdown(
                choices=[
                    "gemini-2.0-flash",
                    "gemini-2.5-flash-preview-04-17",
                    "gemini-2.5-flash-preview-05-20"
                ],
                value="gemini-2.0-flash",
                label="Model",
                elem_id="model-select",
                scale=1
            )
            submit = gr.Button("Send", variant="primary", elem_id="submit-button", scale=1)

    submit.click(
        process_message,
        [msg, effort, model],
        [chat_history_display, msg],  # Added msg to outputs to clear it
        api_name="process_message"
    )

    msg.submit(
        process_message,
        [msg, effort, model],
        [chat_history_display, msg],  # Added msg to outputs to clear it
        api_name="process_message"
    )

demo.launch(server_name="0.0.0.0", server_port=7860, debug=True, inbrowser=True)