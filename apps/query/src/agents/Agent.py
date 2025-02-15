from abc import ABC
from pydantic import BaseModel

class Agent(ABC, BaseModel):
    def run(prompt: str) -> None:
        '''
        Processes the given prompt and executes the agent's logic.
        '''
        pass
