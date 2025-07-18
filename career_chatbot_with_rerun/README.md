This project implements a Gradio-based chatbot designed to represent "Chaoran Zhou" and answer questions related to their career, background, skills, and experience. The chatbot leverages large language models (LLMs) from OpenRouter (specifically `meta-llama/llama-3.3-8b-instruct:free`) for conversational responses and Google's Gemini API (`gemini-2.5-flash-preview-05-20`) for an internal evaluation mechanism.

Key features of the project include:

* **Personalized Responses:** The chatbot is configured with a detailed system prompt that includes a summary and LinkedIn profile content of "Chaoran Zhou" to ensure accurate and in-character responses.
* **Tool Integration:** It utilizes custom tools:
    * `record_user_details`: To capture user email and name for follow-up, steering conversations towards contact.
    * `record_unknown_question`: To log any questions the chatbot cannot answer, regardless of their topic.
* **Self-Correction Mechanism:** An internal "evaluator" LLM (Gemini) assesses the quality and acceptability of the chatbot's responses. If a response is deemed unacceptable, the chatbot attempts to regenerate a better response based on the evaluator's feedback.
* **Gradio Interface:** A user-friendly chat interface is provided using Gradio, allowing for interactive conversations with the AI agent.
* **Pushover Notifications:** The `push` function is integrated to send notifications via Pushover for recorded user details or unanswered questions, providing a real-time alert system.

The project aims to create a professional and engaging AI representative that can faithfully answer inquiries about "Chaoran Zhou" while maintaining quality control and facilitating user engagement.
