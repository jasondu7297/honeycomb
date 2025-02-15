from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph_supervisor import create_supervisor

from agents.AgentRegistry import AgentRegistry
from Workflow import StepState


class GraphBuilder(BaseModel):
    def build(self, model) -> StateGraph:
        # construct all nodes in the graph
        compiled_agents = []
        for agent_cls in AgentRegistry.get_agents():
            compiled_agents.append(agent_cls().build())

        # build a supervisor workflow with all agents and supervisor prompt
        return create_supervisor(
            agents=compiled_agents,
            prompt=self._supervisor_prompt,
            model=model
        )

    _supervisor_prompt: str = '''what is my name?'''
