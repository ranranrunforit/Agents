from pydantic import BaseModel, Field
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel

import os

gemini_client = AsyncOpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=os.getenv('GOOGLE_API_KEY'))

gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash-preview-05-20", openai_client=gemini_client)


HOW_MANY_SEARCHES = 10

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=gemini_model,
    output_type=WebSearchPlan,
)