
This project builds, evaluates, and improves an email assistant. The assistant is designed to automate email management by triaging incoming messages and generating appropriate responses. The project is broken down into four key notebooks that cover the entire lifecycle of developing a robust AI agent.

Key Features and their functionalities include:

1. Foundational Concepts (`langgraph_101.ipynb`)

This notebook introduces the fundamental concepts of LangGraph. It explains how to construct agents and workflows by defining a `State`, creating `Nodes` to update that state, and connecting them with `Edges` to control the flow of logic. It also covers the basics of using tools, persistence with checkpointers, and deploying a LangGraph application.

2. Building the Agent (`agent.ipynb`)

  Here, the primary architecture of the email assistant is built. It consists of:

  A Triage Router: This initial node analyzes an incoming email and classifies it as `respond`, `ignore`, or `notify` using an LLM with structured output capabilities.This project develops an intelligent email assistant from the ground up, demonstrating a full lifecycle from creation to evaluation and enhancement. The multi-stage system is built using the LangGraph agentic framework, powered by Google's Gemini models, and is designed to triage emails, generate responses, allow for human oversight, and learn from user feedback over time.

---
## Key Components and Their Functionalities

* **Agent Architecture (`agent.ipynb`):** This is the core of the assistant, built as a `StateGraph` in LangGraph. It orchestrates the entire email processing workflow.
    * **Triage Router:** This initial node analyzes incoming emails to classify them into one of three categories: `respond`, `ignore`, or `notify`. It utilizes a language model with structured output (`RouterSchema`) to make this decision, preventing the assistant from acting on irrelevant messages.
    * **Response Agent:** For emails requiring a reply, this sub-graph takes over. It operates in a loop, using an `llm_call` node to decide on the next action and a `tool_handler` node to execute it.
    * **Tools:** The agent is equipped with a set of tools defined with the `@tool` decorator, including `write_email`, `schedule_meeting`, and `check_calendar_availability`, which allow it to perform specific actions.

***

* **Evaluation Framework (`evaluation.ipynb`):** This component establishes a robust testing process using the LangSmith platform to ensure the agent's reliability and performance.
    * **Pytest Integration:** The project shows how to write tests using `pytest` and the `@pytest.mark.langsmith` decorator, which logs detailed test results to a LangSmith project. This method is used to verify specific functionalities, like whether the agent calls the correct tools for a given email.
    * **LangSmith Datasets:** It demonstrates how to programmatically create a dataset of email examples and expected outcomes using the `langsmith` client. The agent is then run against this "golden dataset" using `client.evaluate` to measure its performance systematically.
    * **LLM-as-Judge:** An advanced evaluation technique is shown where an LLM is used to grade the agent's final response against a set of predefined success criteria, providing a nuanced assessment of its quality.

***

* **Human-in-the-Loop (HITL) Mechanism (`hitl.ipynb`):** This critical component adds a layer of human oversight to the agent's actions, ensuring user control over sensitive tasks.
    * The graph uses `interrupt` to pause execution at key decision points, such as before sending an email or creating a calendar event.
    * The user is then presented with the agent's proposed action and can choose to `accept`, `edit`, or `ignore` it. The graph is resumed using a `Command` object that communicates the user's decision.
    * A `Question` tool is also introduced, allowing the agent to explicitly ask the user for clarification when it lacks sufficient information to proceed.

***

* **Memory System (`memory.ipynb`):** This component enables the assistant to learn from its interactions and adapt to user preferences over time.
    * The system utilizes **across-thread (long-term) memory** to store persistent knowledge learned from user feedback.
    * An `InMemoryStore` is used to manage this memory, where user preferences are saved under specific namespaces (e.g., "response\_preferences", "cal\_preferences").
    * When a user provides feedback or edits an agent's proposed action via the HITL mechanism, a dedicated memory-updating function is triggered. This function processes the feedback and updates the `Store`.
    * The agent then retrieves these stored preferences during future runs to inform its decisions, leading to more personalized and accurate responses.

***

* **LLM Integration:** All agentic components leverage Google's Gemini models for reasoning, generation, and evaluation.
    * The notebooks specifically mention using `gemini-2.0-flash`.
    * The models are accessed through the `langchain` library's `init_chat_model` function, which provides a standardized interface for interaction.
