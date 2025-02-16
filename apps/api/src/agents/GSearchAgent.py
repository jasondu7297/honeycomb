from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

from config import ProjectConf
from src.agents.Agent import Agent
from src.agents.AgentRegistry import AgentRegistry

@AgentRegistry.register
class GSearchAgent(Agent):
    """
    An example agent that uses the GoogleSearchAPIWrapper via a Tool
    and compiles to a state graph. An agent that leverages Google's Search
    API to retrieve up-to-date web results. Use this agent when you need 
    to obtain recent, relevant information from across the web based on user queries.
    """
    def build(self) -> CompiledStateGraph:
        search = GoogleSearchAPIWrapper()

        google_search_tool = Tool(
            name="GSearchTool",
            description="A tool that interfaces with Google's Search API to fetch the latest " 
                "web results based on user queries. Use this tool when you need to retrieve "
                "up-to-date and relevant information from the web.",
            func=search.run,
        )

        compiled_graph = create_react_agent(name='GSearchAgent', model=ProjectConf.agent_llm, tools=[google_search_tool])

        return compiled_graph
