import os
import io
import pickle
import json
import base64
from typing import Any, Dict, Optional, List
from email.mime.text import MIMEText

from pydantic import PrivateAttr
from langchain.tools import BaseTool

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required by this application.
SCOPES = ["https://mail.google.com/"]

def create_gmail_service_fixed(
    client_secrets_file: str,
    token_file: str = "token.json",
    scopes: Optional[List[str]] = None
):
    """
    Creates a Gmail API service using OAuth with a fixed port (8080).
    """
    if scopes is None:
        scopes = SCOPES

    creds = None
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            creds = flow.run_local_server(port=8080)
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)
    
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender: str, to: str, subject: str, message_text: str) -> str:
    """
    Create a base64url encoded email message.
    """
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return raw.decode()

class GMailTool(BaseTool):
    name: str = "GMailTool"
    description: str = (
        "A tool designed to interact with the Gmail API. It allows you to search for emails,"
        "create draft messages, and send emails. Use this tool for any email-related"
        "operations, such as retrieving, drafting, or sending messages. It supports three operations:\n"
        "1. search_messages:<query> - Search for messages matching the query.\n"
        "2. create_draft:<sender>,<to>,<subject>,<body> - Create a draft message.\n"
        "3. send_message:<sender>,<to>,<subject>,<body> - Send a message.\n\n"
        "Separate the fields with commas. For the message body, if there are commas, "
        "they will be included as part of the body."
    )
    _gmail_service: Any = PrivateAttr()
    
    def __init__(self, client_secrets_file: str, token_file: str = "token.json", **kwargs: Any):
        super().__init__(**kwargs)
        self._gmail_service = create_gmail_service_fixed(client_secrets_file, token_file)
        try:
            profile = self._gmail_service.users().getProfile(userId="me").execute()
            print("Authenticated as:", profile.get("emailAddress"))
        except Exception as e:
            print("Failed to retrieve profile info:", e)
    
    def search_messages(self, query: str) -> List[Dict[str, Any]]:
        """Search for messages matching the given query."""
        results = self._gmail_service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])
        return messages
    
    def create_draft(self, sender: str, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Create a draft email message."""
        raw_message = create_message(sender, to, subject, body)
        draft_body = {"message": {"raw": raw_message}}
        draft = self._gmail_service.users().drafts().create(userId="me", body=draft_body).execute()
        return draft
    
    def send_message(self, sender: str, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send an email message."""
        raw_message = create_message(sender, to, subject, body)
        message = self._gmail_service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        return message
    
    def _run(self, tool_input: str, **kwargs: Any) -> str:
        try:
            if tool_input.startswith("search_messages:"):
                query = tool_input.split(":", 1)[1].strip()
                messages = self.search_messages(query)
                return f"Found {len(messages)} messages:\n" + json.dumps(messages, indent=2)
            
            elif tool_input.startswith("create_draft:"):
                # expected format: create_draft:sender,to,subject,body
                params = tool_input.split(":", 1)[1].split(",")
                if len(params) < 4:
                    return "Error: Provide sender, to, subject, and body separated by commas."
                sender = params[0].strip()
                to = params[1].strip()
                subject = params[2].strip()
                body = ",".join(params[3:]).strip()
                draft = self.create_draft(sender, to, subject, body)
                return "Draft created: " + json.dumps(draft, indent=2)
            
            elif tool_input.startswith("send_message:"):
                # expected format: send_message:sender,to,subject,body
                params = tool_input.split(":", 1)[1].split(",")
                if len(params) < 4:
                    return "Error: Provide sender, to, subject, and body separated by commas."
                sender = params[0].strip()
                to = params[1].strip()
                subject = params[2].strip()
                body = ",".join(params[3:]).strip()
                message = self.send_message(sender, to, subject, body)
                return "Message sent: " + json.dumps(message, indent=2)
            
            else:
                return f"Unsupported operation. Input was: {tool_input}"
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    async def _arun(self, tool_input: str, **kwargs: Any) -> str:
        return self._run(tool_input, **kwargs)


if __name__ == "__main__":
    CLIENT_SECRETS_FILE = os.getenv("GSUITE_CLIENT_SECRETS")
    
    gmail_tool = GMailTool(client_secrets_file=CLIENT_SECRETS_FILE)
    
    # Test search_messages operation.
    print("Testing search_messages operation...")
    search_response = gmail_tool._run("search_messages:subject: Test")
    print("Search Messages Output:\n", search_response, "\n")
    
    # Test create_draft operation.
    print("Testing create_draft operation...")
    draft_response = gmail_tool._run(
        "create_draft:coeus.eng@gmail.com,sairah.amuthan06@gmail.com,Test Draft,This is a test draft message."
    )
    print("Create Draft Output:\n", draft_response, "\n")
    
    # Test send_message operation.
    print("Testing send_message operation...")
    send_response = gmail_tool._run(
        "send_message:coeus.eng@gmail.com,sairah.amuthan06@gmail.com,Test Send,This is a test message."
    )
    print("Send Message Output:\n", send_response, "\n")