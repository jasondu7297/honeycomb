from abc import ABC
from pydantic import BaseModel
from langgraph.graph.state import CompiledStateGraph

class Agent(ABC, BaseModel):
    def build(self) -> CompiledStateGraph:
        pass
