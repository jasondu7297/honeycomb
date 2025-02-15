from abc import ABC
from pydantic import BaseModel

class Agent(ABC, BaseModel):
    def run(self, prompt: str) -> None:
        pass
