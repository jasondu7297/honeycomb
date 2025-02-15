from Agent import Agent
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langgraph.types import Command


class ModelAgent(Agent):
    def run(self, prompt: str) -> None:
        pass