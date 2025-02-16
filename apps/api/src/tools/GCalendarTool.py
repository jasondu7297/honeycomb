import os
import pickle
import json
from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta

from pydantic import PrivateAttr
from langchain.tools import BaseTool

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required by this application.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_calendar_service(
    client_secrets_file: str,
    token_file: str = "calendar_token.pickle",
    scopes: Optional[List[str]] = None
):
    """
    Creates a Google Calendar API service using OAuth with a fixed port (8080).
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
    
    service = build('calendar', 'v3', credentials=creds)
    return service

class GCalendarTool(BaseTool):
    name: str = "GCalendarTool"
    description: str = (
        "A tool for interacting with Google Calendar. It lets you list upcoming events, create new events, "
        "and update existing events using the Calendar API. It supports three operations:\n"
        "1. list_events:<max_results> - List upcoming events from the primary calendar. "
        "If max_results is not provided, defaults to 10.\n"
        "2. create_event:<summary>,<start_time>,<end_time> - Create a new event on the primary calendar. "
        "Times should be in RFC3339 format (e.g., 2023-03-01T09:00:00).\n"
        "3. update_event:<event_id>,<summary>,<start_time>,<end_time> - Update an existing event's summary and times.\n\n"
        "Separate fields with commas."
    )
    _calendar_service: Any = PrivateAttr()
    
    def __init__(self, client_secrets_file: str, token_file: str = "calendar_token.pickle", **kwargs: Any):
        super().__init__(**kwargs)
        self._calendar_service = create_calendar_service(client_secrets_file, token_file)
        # Debug: Print the calendar list to confirm access.
        try:
            calendars = self._calendar_service.calendarList().list().execute()
            primary = next((cal for cal in calendars.get("items", []) if cal.get("primary")), None)
            if primary:
                print("Access granted to primary calendar:", primary.get("summary"))
            else:
                print("No primary calendar found.")
        except Exception as e:
            print("Failed to access calendars:", e)
    
    def list_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = self._calendar_service.events().list(
            calendarId="primary", timeMin=now, maxResults=max_results, singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return events

    def create_event(self, summary: str, start_time: str, end_time: str) -> Dict[str, Any]:
        event = {
            "summary": summary,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }
        created_event = self._calendar_service.events().insert(calendarId="primary", body=event).execute()
        return created_event

    def update_event(self, event_id: str, summary: str, start_time: str, end_time: str) -> Dict[str, Any]:
        event = self._calendar_service.events().get(calendarId="primary", eventId=event_id).execute()
        event["summary"] = summary
        event["start"] = {"dateTime": start_time}
        event["end"] = {"dateTime": end_time}
        updated_event = self._calendar_service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        return updated_event

    def _run(self, tool_input: str, **kwargs: Any) -> str:
        try:
            if tool_input.startswith("list_events:"):
                parts = tool_input.split(":", 1)
                max_results = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 10
                events = self.list_events(max_results)
                return f"Found {len(events)} events:\n" + json.dumps(events, indent=2)
            
            elif tool_input.startswith("create_event:"):
                # expected format: create_event:summary,to,start_time,end_time
                params = tool_input.split(":", 1)[1].split(",")
                if len(params) < 3:
                    return "Error: Provide summary, start_time, and end_time separated by commas."
                summary = params[0].strip()
                start_time = params[1].strip()
                end_time = params[2].strip()
                event = self.create_event(summary, start_time, end_time)
                return "Event created:\n" + json.dumps(event, indent=2)
            
            elif tool_input.startswith("update_event:"):
                # expected format: update_event:event_id,summary,start_time,end_time
                params = tool_input.split(":", 1)[1].split(",")
                if len(params) < 4:
                    return "Error: Provide event_id, summary, start_time, and end_time separated by commas."
                event_id = params[0].strip()
                summary = params[1].strip()
                start_time = params[2].strip()
                end_time = params[3].strip()
                event = self.update_event(event_id, summary, start_time, end_time)
                return "Event updated:\n" + json.dumps(event, indent=2)
            
            else:
                return f"Unsupported operation. Input was: {tool_input}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    async def _arun(self, tool_input: str, **kwargs: Any) -> str:
        return self._run(tool_input, **kwargs)

if __name__ == "__main__":
    CLIENT_SECRETS_FILE = "/Users/sairahamuthan/coeus/client_secrets.json"  
    
    calendar_tool = GCalendarTool(client_secrets_file=CLIENT_SECRETS_FILE)
    
    # Test list_events operation.
    print("Testing list_events operation...")
    list_response = calendar_tool._run("list_events:5")
    print("List Events Output:\n", list_response, "\n")
    
    # Test create_event operation.
    now = datetime.utcnow()
    start = (now + timedelta(hours=1)).isoformat() + "Z"
    end = (now + timedelta(hours=2)).isoformat() + "Z"
    print("Testing create_event operation...")
    create_response = calendar_tool._run(f"create_event:Test Event2,{start},{end}")
    print("Create Event Output:\n", create_response, "\n")
    
    # Test update_event, you need an existing event ID.
    test_event_id = "e4pmv7qqldk2q08o3vcg75kjug"
    print("Testing update_event operation...")
    update_response = calendar_tool._run(f"update_event:{test_event_id},Updated Test Event,{start},{end}")
    print("Update Event Output:\n", update_response, "\n")
