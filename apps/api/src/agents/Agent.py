from abc import ABC
from pydantic import BaseModel
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


class Agent(ABC, BaseModel):
    def build(self) -> CompiledStateGraph:
        pass
