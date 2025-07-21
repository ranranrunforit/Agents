## Agent workflow projects

**[Research Chat](./research_chat)**

This project demonstrates a OpenAI Research Agent workflow using the OpenAI Agents SDK. The agent automates the process of planning, executing, and synthesizing web research, then delivers the results via email.

#### Key Features & Workflow

1. **Planning Searches:**  
   - Uses a `PlannerAgent` (based on the `Agent` class) to generate relevant search queries for a given research topic.
   - Utilizes Pydantic models (`WebSearchItem`, `WebSearchPlan`) for structured outputs.

2. **Web Searching:**  
   - Employs the `WebSearchTool` to perform web searches for each planned query.
   - Results are summarized concisely for further synthesis.

3. **Report Writing:**  
   - A `WriterAgent` creates a detailed markdown report from the search results.
   - Uses another Pydantic model (`ReportData`) for structured report output.

4. **Email Delivery:**  
   - Integrates SendGrid via the `send_email` function (decorated with `@function_tool`) to send the final report as a formatted HTML email.

#### Libraries & Functions Used

- **OpenAI Agents SDK:**  
  - `Agent`, `WebSearchTool`, `Runner`, `trace`, `function_tool`
- **SendGrid:**  
  - For sending emails (`sendgrid.SendGridAPIClient`, `Mail`, `Email`, `To`, `Content`)
- **Asyncio:**  
  - For asynchronous execution of search and report tasks
