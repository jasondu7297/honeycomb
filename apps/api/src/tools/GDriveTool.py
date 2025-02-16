import os
import io
import pickle
import json
from typing import Any, Dict, Optional, List

from pydantic import PrivateAttr
from langchain.tools import BaseTool
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required by this application.
SCOPES = ['https://www.googleapis.com/auth/drive']

def create_drive_service(
    client_secrets_file: str,
    token_file: str = "token.pickle",
    scopes: Optional[List[str]] = None
):
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
            creds = flow.run_local_server(port=8080)  # Force port 8080 bc idk how to deal w dynamic uri's w/ google apis
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)
    
    service = build('drive', 'v3', credentials=creds)
    return service


class GoogleDriveTool(BaseTool):
    name: str = "GDriveTool"
    description: str = (
        "A tool to interact with Google Drive. It can list files, load metadata, "
        "load file content, and update file sharing permissions. "
        "Operations: list_files, load_metadata, load_content, update_sharing."
    )
    # need to use a private attribute to hold the drive service, cause pydantic
    _drive_service: Any = PrivateAttr()
    
    def __init__(self, client_secrets_file: str, token_file: str = "token.pickle", **kwargs: Any):
        super().__init__(**kwargs)
        self._drive_service = create_drive_service(client_secrets_file, token_file)
        # Debug: print logged-in user info using the 'about' endpoint.
        try:
            about_info = self._drive_service.about().get(fields="user").execute()
            user_email = about_info.get("user", {}).get("emailAddress")
            print("Logged in as:", user_email)
        except Exception as e:
            print("Failed to get logged-in user info:", e)
    
    def list_files(self, query: str = "trashed = false", page_size: int = 100) -> List[Dict[str, Any]]:
        results = []
        page_token = None

        #print("Listing files with query:", query)
        
        while True:
            response = self._drive_service.files().list(
                q=query,
                pageSize=page_size,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token
            ).execute()

            #print("Raw API response:", json.dumps(response, indent=2))
            
            results.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        
        return results
    
    def load_metadata(self, file_id: str) -> Dict[str, Any]:
        metadata = self._drive_service.files().get(
            fileId=file_id, fields="*"
        ).execute()
        return metadata
    
    def load_content(self, file_id: str) -> str:
        metadata = self.load_metadata(file_id)
        mime_type = metadata.get("mimeType", "")
        if mime_type.startswith("application/vnd.google-app"):
            request = self._drive_service.files().export_media(
                fileId=file_id,
                mimeType="text/plain"
            )
        else:
            request = self._drive_service.files().get_media(fileId=file_id)
        
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        content = fh.getvalue().decode("utf-8", errors="replace")
        return content
    
    def update_sharing(self, file_id: str, email: str, role: str = "reader") -> Dict[str, Any]:
        permission_body = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        
        permission = self._drive_service.permissions().create(
            fileId=file_id,
            body=permission_body,
            fields='id'
        ).execute()
        
        return permission
    
    def _run(self, tool_input: str, **kwargs: Any) -> str:
        try:
            if tool_input.startswith("list_files"):
                parts = tool_input.split(":", 1)
                query = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "trashed = false"
                files = self.list_files(query=query)
                return f"Found {len(files)} files:\n" + "\n".join([f"{f['name']} (ID: {f['id']})" for f in files])
            
            elif tool_input.startswith("load_metadata:"):
                file_id = tool_input.split(":", 1)[1].strip()
                metadata = self.load_metadata(file_id)
                return json.dumps(metadata, indent=2)
            
            elif tool_input.startswith("load_content:"):
                file_id = tool_input.split(":", 1)[1].strip()
                content = self.load_content(file_id)
                return content
            
            elif tool_input.startswith("update_sharing:"):
                params = tool_input.split(":", 1)[1].split(",")
                if len(params) < 2:
                    return "Error: Provide at least file_id and email. Optionally, a role."
                file_id = params[0].strip()
                email = params[1].strip()
                role = params[2].strip() if len(params) > 2 else "reader"
                permission = self.update_sharing(file_id, email, role)
                return f"Updated sharing, permission ID: {permission.get('id')}"
            
            else:
                return f"Unsupported operation. Input was: {tool_input}"
        
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    async def _arun(self, tool_input: str, **kwargs: Any) -> str:
        return self._run(tool_input, **kwargs)


if __name__ == "__main__":
    CLIENT_SECRETS_FILE = os.getenv("GSUITE_CLIENT_SECRETS")
    
    drive_tool = GoogleDriveTool(client_secrets_file=CLIENT_SECRETS_FILE)
    
    # Test list_files operation.
    print("Testing list_files operation...")
    list_response = drive_tool._run("list_files:")
    print("List Files Output:\n", list_response, "\n")
    
    # To test load_metadata, load_content, and update_sharing, you need a valid file ID.
    test_file_id = "1TK8CD3db6OnVegHDeImx-8K0Y3oFOaLFRQI5fHXZu4k"
    
    # Test load_metadata.
    print("Testing load_metadata operation...")
    metadata_response = drive_tool._run(f"load_metadata:{test_file_id}")
    print("Metadata Output:\n", metadata_response, "\n")
    
    # Test load_content.
    print("Testing load_content operation...")
    content_response = drive_tool._run(f"load_content:{test_file_id}")
    print("Content Output:\n", content_response, "\n")
    
    # Test update_sharing.
    # Provide a test email that you can use.
    test_email = "sairah.amuthan06@gmail.com"
    print("Testing update_sharing operation...")
    sharing_response = drive_tool._run(f"update_sharing:{test_file_id},{test_email},reader")
    print("Update Sharing Output:\n", sharing_response, "\n")