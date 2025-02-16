from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph_supervisor import create_supervisor

from src.agents.AgentRegistry import AgentRegistry
from src.conf.ProjectConf import ProjectConf
from src.utils.prompts import SUPERVISOR_PROMPT

# Necessary for registering classes with AgentRegistry at import time
from src.agents.GSearchAgent import GSearchAgent

class GraphBuilder(BaseModel):
    def build(self) -> StateGraph:
        # construct all nodes in the graph
        compiled_agents = []
        for agent_cls in AgentRegistry.get_agents():
            compiled_agents.append(agent_cls().build())

        # build a supervisor workflow with all agents and supervisor prompt
        return create_supervisor(
            agents=compiled_agents,
            prompt=SUPERVISOR_PROMPT,
            model=ProjectConf.agent_llm
        )
