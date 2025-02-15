import os
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

# wraps the search function in a LangChain Tool.
tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)

if __name__ == "__main__":
    # just an example query
    query = "What is the population of Toronto?"
    result = tool.run(query)
    print("Search Results:\n", result)