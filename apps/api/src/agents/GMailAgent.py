import os

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from src.agents.Agent import Agent
from src.agents.AgentRegistry import AgentRegistry
from config import ProjectConf

from tools.GMailTool import GMailTool

@AgentRegistry.register
class GMailAgent(Agent):
    """
    An agent that interfaces with Gmail to manage email communications. 
    It can search for emails, create draft messages, and send emails. 
    Use this agent when you need to handle email-related tasks such as 
    retrieving, drafting, or sending messages.
    
    This agent supports the following email operations:
      1. search_messages:<query> - Search for messages matching a query.
      2. create_draft:<sender>,<to>,<subject>,<body> - Create a draft email.
      3. send_message:<sender>,<to>,<subject>,<body> - Send an email.
    """
    def build(self) -> CompiledStateGraph:
        gmail_tool_instance = GMailTool(
            client_secrets_file=os.getenv("GSUITE_CLIENT_SECRETS")
        )
        
        def gmail_tool_func(tool_input: str) -> str:
            return gmail_tool_instance._run(tool_input)
        
        gmail_tool = Tool(
            name="GMailTool",
            description=(
                "A tool designed to interact with the Gmail API. It allows you to search "
                "for emails, create draft messages, and send emails. Use this tool for "
                "any email-related operations, such as retrieving, drafting, or "
                "sending messages. Supported operations:\n"
                "1. search_messages:<query> - Search for messages by query.\n"
                "2. create_draft:<sender>,<to>,<subject>,<body> - Create a draft email.\n"
                "3. send_message:<sender>,<to>,<subject>,<body> - Send an email.\n"
                "Format your input accordingly. For example:\n"
                "  send_message:your_email@gmail.com,recipient@example.com,Subject,Message body"
            ),
            func=gmail_tool_func,
        )
        
        compiled_graph = create_react_agent(
            name="GmailAgent",
            model=ProjectConf.agent_llm,
            tools=[gmail_tool],
        )
        return compiled_graph
