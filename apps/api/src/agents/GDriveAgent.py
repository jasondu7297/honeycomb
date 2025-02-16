from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from agents.Agent import Agent
from agents.AgentRegistry import AgentRegistry
from conf.ProjectConf import ProjectConf

from tools.GDriveTool import GoogleDriveTool

@AgentRegistry.register
class GDriveAgent(Agent):
    """
    An agent designed to interact with Google Drive to manage files. 
    It can list files, retrieve file metadata and content, and update 
    sharing permissions. Use this agent when you need to work with 
    files stored on Google Drive, including reading, updating, or sharing them.
    
    This agent supports multiple Google Drive operations:
      - list_files:<optional query> to list files.
      - load_metadata:<file_id> to fetch metadata for a file.
      - load_content:<file_id> to retrieve the content of a file.
      - update_sharing:<file_id>,<email>,<role> to update sharing permissions.
    """
    def build(self) -> CompiledStateGraph:
        # Create an instance of the GoogleDriveTool.
        drive_tool_instance = GoogleDriveTool(
            client_secrets_file="/Users/sairahamuthan/coeus/client_secrets.json"  # Update with your path.
        )
        
        # Define a simple wrapper that delegates input to the tool's _run method.
        def drive_tool_func(tool_input: str) -> str:
            return drive_tool_instance._run(tool_input)
        
        # Wrap our drive tool function in a LangChain Tool.
        google_drive_tool = Tool(
            name="GDriveTool",
            description=(
                "A tool to work with the Google Drive API. It supports listing files,"
                "retrieving file metadata and content, and updating sharing permissions."
                "Use this tool when you need to manage files stored in Google Drive."
                "Supported operations include:\n"
                "1. list_files:<optional query> to list files (e.g., 'list_files:' or 'list_files:name contains report').\n"
                "2. load_metadata:<file_id> to fetch metadata for a file.\n"
                "3. load_content:<file_id> to retrieve the content of a file.\n"
                "4. update_sharing:<file_id>,<email>,<role> to update a file's sharing permissions (e.g., 'update_sharing:FILE_ID,user@example.com,reader').\n"
                "Format your input exactly as shown."
            ),
            func=drive_tool_func,
        )
        
        compiled_graph = create_react_agent(
            name="GDriveAgent",
            model=ProjectConf.agent_llm,
            tools=[google_drive_tool],
        )
        
        return compiled_graph
