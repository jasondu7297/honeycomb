from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

from agents.Agent import Agent
from agents.AgentRegistry import AgentRegistry
from conf.ProjectConf import ProjectConf

@AgentRegistry.register
class GSearchAgent(Agent):
    """
    An example agent that uses the GoogleSearchAPIWrapper via a Tool
    and compiles to a state graph.
    """
    def build(self) -> CompiledStateGraph:
        # Create the GoogleSearchAPIWrapper
        search = GoogleSearchAPIWrapper()

        # Wrap it in a Tool
        google_search_tool = Tool(
            name="google_search",
            description="Use this tool to search Google for recent results.",
            func=search.run,
        )

        # Create a ReAct-style agent with our search tool
        compiled_graph = create_react_agent(name='GSearchAgent', model=ProjectConf.agent_llm, tools=[google_search_tool])

        return compiled_graph
