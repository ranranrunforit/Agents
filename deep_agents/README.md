This project builds a "Deep Agent" using LangGraph. It builds a sophisticated, stateful AI agent capable of handling complex, long-running tasks.

The core idea is to move beyond a simple ReAct (Reasoning and Acting) loop and implement more advanced patterns used in production-grade agent systems. Each notebook introduces a new concept that solves a common problem in agent design:

1.  **Stateful Agents (`0_create_agent.ipynb`):** Establishes the foundation of a stateful agent using LangGraph, showing how to manage state and use basic tools.

2.  **Planning & Task Tracking (`1_todo.ipynb`):** Solves the problem of "context rot" (the agent forgetting its goal) by implementing a **TODO list**. This gives the agent a plan to create and follow.

3.  **Context Offloading (`2_files.ipynb`):** Solves the problem of limited context windows by implementing a **virtual filesystem**. This allows the agent to "offload" large pieces of information (like search results or documents) to memory and read them back as needed.

4.  **Context Isolation (`3_subagents.ipynb`):** Solves the problem of "context contamination" by introducing a **supervisor/sub-agent architecture**. The main agent delegates specific tasks to specialized sub-agents that run in their own isolated context, preventing them from interfering with the main agent's plan.

5.  **Deep Agent for Search (`4_full_agent.ipynb`):** combines all these patterns into a single, powerful "Deep Agent" that can plan, delegate, use a filesystem for memory, and reflect on its actions to solve a complex research query.
