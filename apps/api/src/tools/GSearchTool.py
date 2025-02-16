import os
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

# wraps the search function in a LangChain Tool.
tool = Tool(
    name="GSearchTool",
    description="A tool that interfaces with Google's Search API to fetch the latest" 
                "web results based on user queries. Use this tool when you need to retrieve"
                "up-to-date and relevant information from the web.",
    func=search.run,
)

if __name__ == "__main__":
    # just an example query
    query = "What is the population of Toronto?"
    result = tool.run(query)
    print("Search Results:\n", result)