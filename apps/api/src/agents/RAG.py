from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from langchain_core.tools import Tool

from agents.Agent import Agent
from agents.AgentRegistry import AgentRegistry
from conf.ProjectConf import ProjectConf

from memory.service import get_knn

def run_rag(query: str) -> str:
    results = get_knn(query, k=5)
    return str(results)


@AgentRegistry.register
class RAGAgent(Agent):
    """
    An agent that runs RAG against our Elasticserarch VectorDB.

    The output will be a string of the text of the K nearest neighbours
    """
    def build(self) -> CompiledStateGraph:
        # Wrap it in a Tool
        rag_tool = Tool(
            name="k_nearest_neighbours",
            description="Use this tool to search the user's chat history. The output will be a string of the plain text of the K nearest neighbours",
            func=run_rag,
        )

        # Create a ReAct-style agent with our search tool
        compiled_graph = create_react_agent(name='RAGAgent', model=ProjectConf.agent_llm, tools=[rag_tool])

        return compiled_graph
