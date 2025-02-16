from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from agents.Agent import Agent
from agents.AgentRegistry import AgentRegistry
from config import ProjectConf

@AgentRegistry.register
class HumanInLoopAgent(Agent):
    """    
    This agent is designed to demonstrate a "human in the loop" process.
    It registers a tool that directly asks the user for input via the console (or
    any other UI hook). You can customize the logic of when or how often the agent
    calls this tool (in the LLM prompts, for example).
    """

    def build(self) -> CompiledStateGraph:

        # A sample tool that explicitly asks for human input:
        def ask_for_human_input(prompt: str) -> str:
            """
            Ask the user for input or confirmation. 
            In a real-world scenario, this might connect to a UI or a chat interface
            rather than just input().
            """
            user_response = input(f"[Human in the loop] {prompt}\nYour response: ")
            return user_response

        # Register our tool for the agent to use:
        human_input_tool = Tool(
            name="ask_for_human_input",
            func=ask_for_human_input,
            description=(
                "Use this tool to ask for explicit human guidance or confirmation. "
                "For example, if you're very unsure about how to proceed or need user approval."
            ),
        )

        # Create a ReAct agent that can call our custom tool:
        compiled_graph = create_react_agent(
            name="HumanInLoopAgent",
            model=ProjectConf.agent_llm,
            tools=[human_input_tool],
        )

        return compiled_graph
