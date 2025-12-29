# app/agent/moderation_agent.py
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import create_openai_functions_agent

from app.agent.prompt import PROMPT
from app.agent.tools import mark_safe, mark_hidden, mark_review



def build_moderation_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        base_url=os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1"),
        api_key=os.getenv("VLLM_API_KEY", "EMPTY"),
        model=os.getenv("VLLM_MODEL", "qwen3-4b"),
        temperature=0.1,
    )

    tools = [mark_safe, mark_hidden, mark_review]

    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=PROMPT)

    return AgentExecutor(agent=agent, tools=tools, verbose=False)
