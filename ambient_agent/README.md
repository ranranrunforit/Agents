
This project builds, evaluates, and improves an email assistant. The assistant is designed to automate email management by triaging incoming messages and generating appropriate responses. The project is broken down into four key notebooks that cover the entire lifecycle of developing a robust AI agent.

Key Features and Concepts
1. Foundational Concepts (`langgraph_101.ipynb`)
This notebook introduces the fundamental concepts of LangGraph. It explains how to construct agents and workflows by defining a `State`, creating `Nodes` to update that state, and connecting them with `Edges` to control the flow of logic. It also covers the basics of using tools, persistence with checkpointers, and deploying a LangGraph application.

2. Building the Core Agent (`agent.ipynb`)
Here, the primary architecture of the email assistant is built. It consists of:

A Triage Router: This initial node analyzes an incoming email and classifies it as `respond`, `ignore`, or `notify` using an LLM with structured output capabilities.

A Response Agent: If an email needs a reply, it is passed to this agent, which is a sub-graph that operates in a loop. The agent uses a set of predefined tools like `write_email`, `schedule_meeting`, and `check_calendar_availability` to fulfill the user's request.

3. Evaluating the Agent (`evaluation.ipynb`)
This notebook focuses on testing the agent's performance. It showcases two main evaluation methods:

Pytest Integration: Writing tests using `pytest` and the `@pytest.mark.langsmith` decorator to run specific test cases and log the results to a LangSmith project.

LangSmith Datasets: Programmatically creating a dataset in LangSmith with email inputs and expected outputs, and then running the agent against this dataset using the `client.evaluate` function.

LLM-as-Judge: An advanced evaluation technique is introduced where another LLM is used to grade the agent's response based on a set of predefined criteria.

4. Adding Human-in-the-Loop (`hitl.ipynb`)
To ensure safety and user control, this notebook adds Human-in-the-Loop (HITL) functionality.

The graph is modified to `interrupt` execution before performing critical actions, such as sending an email or scheduling a meeting.

The user can then review the agent's proposed action and choose to accept, edit, or ignore it. The workflow resumes based on this input using a `Command` object.

A new `Question` tool is introduced, allowing the agent to pause and ask the user for clarification when needed.

5. Implementing Memory (`memory.ipynb`)
The final notebook enhances the agent by giving it long-term memory.

It explains the difference between thread-scoped (short-term) and across-thread (long-term) memory.

An `InMemoryStore` is used to persist user preferences learned from HITL interactions. For instance, if a user edits an email to be less formal, this preference is saved.

The agent's prompts are updated to retrieve and incorporate these saved memories, allowing it to learn from feedback and adapt its behavior to the user's style over time.
