from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from agents.Agent import Agent
from agents.AgentRegistry import AgentRegistry
from config import ProjectConf

from tools.GCalendarTool import GCalendarTool

@AgentRegistry.register
class GCalendarAgent(Agent):
    """
    An agent that leverages the GCalendarTool to manage calendar events. Use it to view, 
    schedule, and modify events on Google Calendar.
    
    This agent supports operations including:
      1. list_events:<max_results> - List upcoming events from the primary calendar.
      2. create_event:<summary>,<start_time>,<end_time> - Create a new calendar event.
      3. update_event:<event_id>,<summary>,<start_time>,<end_time> - Update an existing event.
    
    Use this agent for tasks that involve reading, creating, or updating events in Google Calendar.
    """
    def build(self) -> CompiledStateGraph:
        calendar_tool_instance = GCalendarTool(
            client_secrets_file = os.getenv("GSUITE_CLIENT_SECRETS")
        )
        
        def calendar_tool_func(tool_input: str) -> str:
            return calendar_tool_instance._run(tool_input)
        
        calendar_tool = Tool(
            name="GCalendarTool",
            description=(
                "A tool for interacting with Google Calendar. It lets you list upcoming events, "
                "create new events, and update existing events using the Calendar API. Supported operations:\n"
                "1. list_events:<max_results> - List upcoming events (default max_results=10).\n"
                "2. create_event:<summary>,<start_time>,<end_time> - Create a new event. "
                "Times must be in RFC3339 format (e.g., 2023-03-01T09:00:00Z).\n"
                "3. update_event:<event_id>,<summary>,<start_time>,<end_time> - Update an existing event.\n"
                "Format your input as shown."
            ),
            func=calendar_tool_func,
        )
        
        compiled_graph = create_react_agent(
            name="GCalendarAgent",
            model=ProjectConf.agent_llm,
            tools=[calendar_tool],
        )
        return compiled_graph
