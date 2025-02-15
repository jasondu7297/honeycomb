import os
from langchain_googledrive.tools.google_drive.tool import GoogleDriveSearchTool
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Retrieve credentials file path from environment.
GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH")
if not GOOGLE_CREDENTIALS_PATH:
    raise ValueError("The GOOGLE_CREDENTIALS_PATH environment variable is not set.")

# Perform the OAuth flow to get credentials.
flow = InstalledAppFlow.from_client_secrets_file(
    GOOGLE_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)
credentials = flow.run_local_server(port=8888)

# Now, if the tool accepts credentials directly (check its docs):
tool = GoogleDriveSearchTool(api_wrapper={"credentials": credentials})
# or if the tool supports a 'credentials' parameter:


if __name__ == "__main__":
    search_query = "Jason"  # Adjust query as needed.
    output = tool._run(search_query)
    formatted_output = " ".join(output.split())
    print("Search Result:\n", formatted_output)