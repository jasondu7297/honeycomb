from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph_supervisor import create_supervisor

from config import ProjectConf
from src.agents.AgentRegistry import AgentRegistry
from src.utils.prompts import SUPERVISOR_PROMPT

# Necessary for registering classes with AgentRegistry at import time
from src.agents import (
    GSearchAgent,
    RAGAgent
) # noqa: F401

class GraphBuilder:
    _graph: CompiledStateGraph

    @classmethod
    def get_graph(cls) -> CompiledStateGraph:
        return cls._graph

    @classmethod
    def build(cls) -> CompiledStateGraph:
        # construct all nodes in the graph
        compiled_agents = []
        for agent_cls in AgentRegistry.get_agents():
            compiled_agents.append(agent_cls().build())

        # build a supervisor workflow with all agents and supervisor prompt
        graph = create_supervisor(
            agents=compiled_agents,
            prompt=SUPERVISOR_PROMPT,
            model=ProjectConf.agent_llm
        )

        # deploy a checkpointer for rollback and branching features
        checkpointer = MemorySaver()

        # return a compiled graph with checkpointing
        cls._graph = graph.compile(checkpointer=checkpointer)
        return cls._graph
