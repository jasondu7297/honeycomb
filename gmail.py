import os
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

# Step 1: Set environment variables (if needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sairahamuthan/coeus/client_secrets.json"

# Step 2: Get Gmail credentials (Interactive flow if token.json doesn't exist)
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="/Users/sairahamuthan/coeus/client_secrets.json",
    redirect_port=8080,
)

# Step 3: Build Gmail API resource
api_resource = build_resource_service(credentials=credentials)

# Step 4: Instantiate Gmail Toolkit
toolkit = GmailToolkit(api_resource=api_resource)

# Step 5: List available Gmail tools
tools = toolkit.get_tools()
print("\n📧 Available Gmail Tools:")
for tool in tools:
    print(f"- {tool.name}: {tool.description}")

# Step 6: Search Gmail for emails containing a specific keyword
gmail_search_tool = next(
    (tool for tool in tools if tool.name == "GmailSearch"), None
)

if gmail_search_tool:
    query = "from:no-reply@google.com"
    print(f"\n🔍 Searching Gmail for: '{query}'...")
    search_results = gmail_search_tool.run(query)
    if search_results:
        for i, result in enumerate(search_results, 1):
            print(f"\n📬 Email {i}:")
            print(f"Subject: {result.get('subject', 'No Subject')}")
            print(f"Snippet: {result.get('snippet', 'No Snippet')}")
            print(f"Thread ID: {result.get('threadId')}")
    else:
        print("No emails found for the query.")
else:
    print("GmailSearch tool not found.")
