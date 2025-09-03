This project using LangSmith to develop, test, and monitor LLM applications in production. It implements a RAG (Retrieval Augmented Generation) system that answers questions about LangSmith documentation.

## Structure

### Module 0: Setup
- **0_rag_application.ipynb**: Sets up basic RAG application using Google's Gemini model with LangSmith tracing enabled

### Module 1: Visibility While Building with Tracing
- **1_tracing_basics.ipynb**: Introduction to tracing concepts in LangSmith
- **3_alternative_tracing_methods.ipynb**: Different ways to implement tracing
- **4_conversational_threads.ipynb**: Managing conversation threads with tracing

### Module 2: Testing and Evaluation
- **1_dataset_upload.ipynb**: How to upload and manage datasets in LangSmith
- **2_evaluators.ipynb**: Creating custom evaluators for LLM outputs
- **3_experiments.ipynb**: Running experiments with different model configurations
- **4_pairwise_experiments.ipynb**: Comparing different model/prompt pairs
- **5_summary_evaluators.ipynb**: Building evaluators for summarization tasks

### Module 3: Prompt Engineering
- **1_playground_experiments.ipynb**: Experimenting with prompts in LangSmith
- **2_prompt_hub.ipynb**: Using the LangSmith Prompt Hub
- **3_prompt_engineering_lifecycle.ipynb**: End-to-end prompt development workflow

### Module 4: Collecting Human Feedback
- **publishing_feedback.ipynb**: How to collect and publish human feedback on model outputs

### Module 5: Production Observability
- **1_filtering.ipynb**: Filtering and analyzing production traces
- **2_online_evaluation.ipynb**: Real-time evaluation of production models

## Key Features
- Implements RAG using LangSmith documentation as knowledge base
- Demonstrates tracing and monitoring capabilities
- Shows how to evaluate and test LLM applications
- Covers prompt engineering workflow
- Includes production monitoring features

## Project Structure
```
images/                    # Diagrams and images
module_0_setup/            # Initial setup and basic RAG
module_1_visibility.../    # Tracing implementation
module_2_testing.../       # Testing and evaluation
module_3_prompt.../        # Prompt engineering
module_4_collecting.../    # Feedback collection
module_5_production.../    # Production monitoring
```

