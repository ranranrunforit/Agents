The project is developed progressively across several notebooks, culminating in a fully integrated multi-agent research system using LangGraph, LangChain, and the Model Context Protocol (MCP).


* **Initial Scoping and Architecture (`1_scoping.ipynb`)**
    * This notebook lays the groundwork for the project, introducing the **plan-and-execute** agent architecture.
    * It defines the initial `AgentState` using `TypedDict` and introduces the concept of a **Supervisor** agent that will orchestrate the overall workflow.


* **Research Agent (`2_research_agent.ipynb`)**
    * This notebook builds the primary worker agent, the `ResearchAgent`.
    * This agent is responsible for taking a single, specific research task, executing a web search using the `TavilySearchResults` tool, and generating a concise summary of the findings.
    * The agent is constructed as a self-contained `StateGraph` in LangGraph, with logic to call the LLM, which in turn can use the search tool.
 

* **Agent Integration (`3_research_agent_mcp.ipynb`)**
    * This notebook explores integration patterns by wraping a research agent as a Model-as-Controller Protocol (MCP) server.
    * This turns the entire agent into a callable tool, enabling more complex, hierarchical agent structures where a supervisor can delegate tasks to specialized sub-agents.


* **Research Supervisor (`4_research_supervisor.ipynb`)**
    * This notebook implements the central orchestrator, the `ResearchSupervisor`.
    * The supervisor takes the initial user query and uses an LLM to create a multi-step research plan.
    * It manages the overall workflow by using a conditional edge in its `StateGraph`. Based on the current state, it decides whether to call a researcher, another tool, or conclude the process and generate the final report.


* **Full Multi-Agent System (`5_full_agent.ipynb`)**
    * This notebook integrates all the components into the final, cohesive application.
    * It demonstrates the complete workflow where the `ResearchSupervisor` acts as the manager, breaking down the query and delegating specific search tasks to the `ResearchAgent` by calling it as a tool.
    * The supervisor collects the results from each research step and uses them to generate the final, comprehensive report for the user.


* **Shared Utilities (`utils.py`)**
    * This file contains shared code used across the notebooks to maintain consistency and reduce redundancy.
    * It includes the definition for the shared `AgentState`, helper functions for creating tool nodes, and other utility functions.
 

## Directory Structure

```

notebooks/                                # Notebooks and utility scripts
src/deep_research_from_scratc/            # Generated code. All `.py` files here are written by the notebooks via `%%writefile`.
langgraph.json                            # LangGraph workflow configuration.
pyproject.toml                            # Project dependencies

```

