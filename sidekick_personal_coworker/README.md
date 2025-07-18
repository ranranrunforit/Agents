This project develops a chatbot application using Gradio, designed to execute tasks based on user requests, leverage tools, and self-correct to meet predefined success criteria. The system integrates various tools and an internal evaluation mechanism to ensure effective and self-correcting operation. 

The core components and functionalities of the Sidekick project include:
* **Gradio User Interface:** The `app.py` file sets up a Gradio-based web interface, featuring a chatbot display, input fields for user messages and success criteria, and buttons for initiating tasks ("Go!") and resetting the conversation. 
* **Sidekick Agent (`sidekick.py`):** This is the main orchestrator of the system. It initializes and manages the LLMs and tools, and defines the state and workflow of the RAG system.
    * **Worker LLM:** Utilizes a `ChatGoogleGenerativeAI` model (specifically `gemini-2.5-flash-preview-05-20`) bound with various tools to process user requests and generate responses. 
    * **Evaluator LLM:** Another `ChatGoogleGenerativeAI` model (`gemini-2.0-flash`) acts as an internal evaluator. It assesses the worker's responses against the defined success criteria, provides feedback, and determines if the task is complete or if further user input is needed. 
    * **Self-Correction:** The system is designed to self-correct; if the evaluator deems a response unsatisfactory, the worker LLM receives feedback and attempts to regenerate a better response. 
    * **State Management:** The `State` TypedDict tracks the conversation history, success criteria, feedback on work, and flags for success criteria met or user input needed. 
* **Integrated Tools (`sidekick_tools.py`):** The Sidekick agent is equipped with a variety of tools to interact with external systems and perform tasks:
    * **Web Browse:** `PlayWrightBrowserToolkit` enables the agent to browse and interact with web pages. 
    * **Push Notifications:** A `send_push_notification` tool, utilizing Pushover, allows the agent to send alerts or messages. 
    * **File Management:** `FileManagementToolkit` provides capabilities for managing files within a sandbox directory. 
    * **Web Search:** `GoogleSerperAPIWrapper` facilitates online web searches. 
    * **Wikipedia Queries:** `WikipediaQueryRun` enables the agent to query Wikipedia for information. 
    * **Python REPL:** A `PythonREPLTool` allows the agent to execute Python code. 
* **Graph-based Workflow:** The system's logic is built using `langgraph.graph.StateGraph`, defining a flow where the worker generates responses, which are then routed to tools if needed, or to the evaluator for assessment. Based on the evaluation, the process either loops back to the worker for refinement or terminates. 
* **Resource Management:** The application includes functions to set up and free resources, specifically closing the Playwright browser and stopping the Playwright instance when no longer needed, ensuring efficient resource utilization. 
