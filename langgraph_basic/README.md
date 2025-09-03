The project builds and manages AI-powered assistants using LangGraph. It creates modular, configurable, and versioned assistants that can manage tasks, interact with users, and maintain persistent state. The project is structured into modules, each focusing on a specific concept or feature of LangGraph.

## Module 0: Basics

- **`basics.ipynb`**:  
  Introduces LangGraph, its motivation, and the course structure. Explains the need for graph-based agent control and sets up the environment for subsequent modules.

---

## Module 1: Foundations

- **`simple_graph.ipynb`**:  
  Builds a minimal graph with three nodes and a conditional edge, demonstrating the basics of graph construction in LangGraph.

- **`agent.ipynb`**:  
  Implements a simple agent that can act, observe, and reason using tools, showing how to integrate LLMs and tool calls in a graph.

- **`chain.ipynb`**:  
  Demonstrates chaining nodes for sequential processing, introducing the concept of chaining LLM calls and tool outputs.

- **`router.ipynb`**:  
  Shows how to route between different nodes based on input, using conditional logic to direct the flow in the graph.

- **`deployment.ipynb`**:  
  Covers deploying LangGraph applications locally and to LangGraph Cloud, including integration with LangSmith and Studio.

---

## Module 2: State and Memory

- **`state_schema.ipynb`**:  
  Explains how to define and customize the state schema for graph nodes, enabling structured data flow.

- **`state_reducers.ipynb`**:  
  Introduces state reducers for updating and managing state transitions within the graph.

- **`multiple_schemas.ipynb`**:  
  Demonstrates using multiple schemas for different nodes or stages, allowing for more flexible and modular graph design.

- **`trim_filter_messages.ipynb`**:  
  Shows advanced techniques for trimming and filtering messages in the graph state to manage memory and token usage.

- **`chatbot_summarization.ipynb`**:  
  Implements a chatbot that summarizes conversation history using LLMs, enabling long-running conversations with compressed memory.

- **`chatbot_external_memory.ipynb`**:  
  Integrates external memory storage for chatbots, persisting conversation history and supporting long-term context.

---

## Module 3: Human-in-the-Loop & Debugging

- **`breakpoints.ipynb`**:  
  Introduces breakpoints to pause graph execution for human approval, enabling human-in-the-loop workflows.

- **`dynamic_breakpoints.ipynb`**:  
  Expands on breakpoints with dynamic logic, allowing for conditional interruption and debugging.

- **`edit_state_human_feedback.ipynb`**:  
  Demonstrates editing graph state at breakpoints, incorporating human feedback and state modification during execution.

- **`streaming_interruption.ipynb`**:  
  Covers streaming outputs and interrupting execution, providing real-time feedback and control.

- **`time_travel.ipynb`**:  
  Shows how to rewind and replay graph execution for debugging and reproducibility.

---

## Module 4: Multi-Agent & Research Assistant

- **`parallelization.ipynb`**:  
  Demonstrates parallel node execution for multi-agent workflows, improving efficiency and scalability.

- **`sub_graph.ipynb`**:  
  Introduces sub-graphs for modular and hierarchical graph design, useful for complex multi-agent systems.

- **`map_reduce.ipynb`**:  
  Implements map-reduce patterns in LangGraph, enabling distributed processing and aggregation.

- **`research_assistant.ipynb`**:  
  Combines previous concepts to build a multi-agent research assistant, integrating parallelization, sub-graphs, and memory.

---

## Module 5: Long-Term Memory

- **`memory_store.ipynb`**:  
  Introduces the LangGraph Memory Store for persistent, cross-thread memory using key-value stores (e.g., Postgres, Redis).

- **`memoryschema_profile.ipynb`**:  
  Defines and uses a profile schema for storing user-specific long-term memory.

- **`memoryschema_collection.ipynb`**:  
  Implements a collection schema for managing lists of memories (e.g., ToDos) and demonstrates saving/retrieving them.

- **`memory_agent.ipynb`**:  
  Builds an agent with long-term memory, capable of updating user profiles, ToDo collections, and its own instructions.

---

## Module 6: Deployment & Assistants

- **`assistant.ipynb`**:  
  Demonstrates the use of LangGraph "assistants"—versioned, configurable agents. Shows how to create, update, search, and delete assistants using the SDK, and how to interact with them for different task categories (e.g., personal vs. work ToDos).

- **`connecting.ipynb`**:  
  Explains connecting to a deployed LangGraph server, using the SDK to interact with threads, runs, and the memory store.

---

## Studio Integration

Each module contains a `studio/` directory with a langgraph.json file, mapping graph names to Python files for use with [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio), enabling visual editing and deployment.


