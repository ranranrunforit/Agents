This project using LangSmith to develop, test, and monitor LLM applications in production. It implements a RAG (Retrieval Augmented Generation) system that answers questions about LangSmith documentation.

## Structure

### [Module 0: Setup](./module_0_setup)
- **`0_rag_application.ipynb`**: Sets up basic RAG application using Google's Gemini model with LangSmith tracing enabled

### [Module 1: Visibility While Building with Tracing](./module_1_visibility_while_building_with_tracing)
- **`1_tracing_basics.ipynb`**: Introduction to tracing concepts in LangSmith
- **`2_types_of_runs`**: Different ways to implement tracing
- **`3_alternative_tracing_methods.ipynb`**: Different ways to implement tracing
- **`4_conversational_threads.ipynb`**: Managing conversation threads with tracing

### [Module 2: Testing and Evaluation](./module_2_testing_and_evaluation)
- **`1_dataset_upload.ipynb`**: How to upload and manage datasets in LangSmith
- **`2_evaluators.ipynb`**: Creating custom evaluators for LLM outputs
- **`3_experiments.ipynb`**: Running experiments with different model configurations
- **`4_pairwise_experiments.ipynb`**: Comparing different model/prompt pairs
- **`5_summary_evaluators.ipynb`**: Building evaluators for summarization tasks

### [Module 3: Prompt Engineering](./module_3_prompt_engineering)
- **`1_playground_experiments.ipynb`**: Experimenting with prompts in LangSmith
- **`2_prompt_hub.ipynb`**: Using the LangSmith Prompt Hub
- **`3_prompt_engineering_lifecycle.ipynb`**: End-to-end prompt development workflow

### [Module 4: Collecting Human Feedback](./module_4_collecting_human_feedback)
- **`publishing_feedback.ipynb`**: How to collect and publish human feedback on model outputs

### [Module 5: Production Observability](./module_5_production_observability)
- **`1_filtering.ipynb`**: Filtering and analyzing production traces
- **`2_online_evaluation.ipynb`**: Real-time evaluation of production models

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

