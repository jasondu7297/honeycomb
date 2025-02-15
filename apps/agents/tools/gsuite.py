import os
from langchain_google_community import GoogleDriveLoader  # Updated import
from langchain.tools import BaseTool
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Retrieve the credentials path from an environment variable.
GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH")
if not GOOGLE_CREDENTIALS_PATH:
    raise ValueError("The GOOGLE_CREDENTIALS_PATH environment variable is not set.")

class GoogleDriveSearchTool(BaseTool):
    name: str = "GoogleDriveSearchTool"
    description: str = (
        "Searches Google Drive for files with names containing the given query and "
        "returns the content of the first matching file."
    )

    def _run(self, query: str) -> str:
        try:
            # Run the OAuth flow with a fixed port (adjust as needed).
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=["https://www.googleapis.com/auth/drive.readonly"]
            )
            credentials = flow.run_local_server(port=8888)

            drive_service = build('drive', 'v3', credentials=credentials)

            # Build the search query.
            search_query = f"name contains '{query}'"
            results = drive_service.files().list(
                q=search_query,
                fields="files(id, name)",
                pageSize=1
            ).execute()

            files = results.get("files", [])
            if not files:
                return f"No files found matching the query: {query}"

            file_id = files[0]["id"]

            # Use the updated GoogleDriveLoader to load the document.
            loader = GoogleDriveLoader(credentials=credentials, file_ids=[file_id])
            documents = loader.load()

            if not documents:
                return "Found file but could not load its content."

            return documents[0].page_content

        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Asynchronous operation is not implemented.")

# Example usage:
if __name__ == "__main__":
    tool = GoogleDriveSearchTool()
    search_query = "Jason Du"  # Adjust query as needed.
    output = tool._run(search_query)
    formatted_output = output.replace("\n", "")
    print("Search Result:\n", formatted_output)

