from typing import Type

from agents.Agent import Agent

class AgentRegistry:
    # Class-level mapping of all agent string representation to agent class
    _registry: list[Type[Agent]] = []

    @classmethod
    def register(cls, agent_cls: Type['Agent']) -> Type['Agent']:
        '''Decorator method to register a given agent with the registry'''
        if agent_cls in cls._registry:
            raise ValueError(f"{agent_cls.__name__} is already registered.")
        cls._registry.append(agent_cls)
        return agent_cls

    @classmethod
    def get_agents(cls) -> list[Agent]:
        '''Returns all agents for graph construction'''
        return cls._registry
