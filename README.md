## Agent Workflow Projects

**[Research Chat](./research_chat)**

This project demonstrates a Research Agent workflow using the OpenAI Agents SDK. The agent automates the process of planning, executing, and synthesizing web research, then delivers the results via email.

#### Key Features & Workflow

- Uses a `PlannerAgent` (based on the `Agent` class) to generate relevant search queries for a given research topic.  
- Employs the `WebSearchTool` to perform web searches for each planned query.
- A `WriterAgent` creates a detailed markdown report from the search results.
- Integrates SendGrid via the `send_email` function (decorated with `@function_tool`) to send the final report as a formatted HTML email.

#### Libraries & Functions Used

- **OpenAI Agents SDK:** `Agent`, `WebSearchTool`, `Runner`, `trace`, `function_tool`
- **SendGrid:** For sending emails (`sendgrid.SendGridAPIClient`, `Mail`, `Email`, `To`, `Content`)
- **Asyncio:** For asynchronous execution of search and report tasks


****
**[Career Conversation with Rerun](./career_conversation_with_rerun)**

This project implements a professional chatbot web application using Gradio, OpenAI, and Pushover APIs. The chatbot represents AI representative and answers questions about his career, background, and experience. It loads profile and summary data from local files and uses the OpenAI GPT-4o-mini model for conversation. The app supports function calling for two tools: recording user contact details and logging unanswered questions. Push notifications are sent via the Pushover API when these tools are triggered.

**Key Libraries and Functions Used:**
- `gradio` (`gr.ChatInterface`): Builds the interactive web chat UI.
- `openai` (`OpenAI`): Handles LLM chat completions and function calling.
- `pypdf` (`PdfReader`): Reads and extracts text from PDF profile files.
- `requests`: Sends push notifications to Pushover.
- Custom functions: `record_user_details`, `record_unknown_question`, and `push`.

