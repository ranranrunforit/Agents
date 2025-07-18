This project implements a Gemini-powered research assistant with a Gradio interface, designed to answer user questions by performing web research. The system leverages a multi-step research process, including query generation, web searching, reflection, and answer finalization, all orchestrated using LangGraph.

Key features and components of the project include:

* **Gradio User Interface (`app.py`):** Provides an interactive chat interface where users can input questions, select a research "effort" level (low, medium, high), and choose a Gemini model for the research process. The chat history is displayed dynamically, showing the progress of the research.
* **Research Agent Graph (`graph.py`):** The core of the research assistant, built with LangGraph. It defines a state machine that progresses through several nodes:
    * **`generate_query`:** Generates initial web search queries based on the user's question and the selected "effort" level, using a Gemini model (`query_writer_instructions` from `prompts.py`).
    * **`web_research`:** Executes web searches using the generated queries. It uses the Gemini API with Google Search capabilities to retrieve information, resolves URLs for citations, and inserts citation markers into the summarized results.
    * **`reflection`:** Evaluates the gathered research results. A Gemini model (`reflection_instructions` from `prompts.py`) determines if the information is sufficient to answer the user's question or if there are knowledge gaps requiring follow-up queries. This node controls the research loop.
    * **`finalize_answer`:** Compiles the gathered information into a comprehensive answer, including citations, using a Gemini model (`answer_instructions` from `prompts.py`).
* **Configuration (`configuration.py`):** Defines configurable parameters for the agent, such as the models used for query generation, reflection, and answering, as well as the number of initial queries and maximum research loops. These parameters can be adjusted via the Gradio interface.
* **State Management (`state.py`):** Defines the `OverallState` TypedDict, which tracks the conversation messages, search queries, web research results, gathered sources, and research loop parameters throughout the graph's execution.
* **Prompt Engineering (`prompts.py`):** Contains carefully crafted prompts for each stage of the research process (query writing, web searching, reflection, and answer generation) to guide the Gemini models effectively.
* **Utility Functions (`utils.py`):** Provides helper functions for extracting research topics, resolving URLs for consistent citations, inserting citation markers into text, and processing Gemini model responses to extract grounding information.
* **Robustness:** The `graph.py` includes a `try_all_clients` function to handle API rate limits and errors by attempting the API call with multiple Gemini API keys, ensuring higher reliability.
