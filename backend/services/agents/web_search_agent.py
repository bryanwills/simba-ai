from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field


# Pydantic model for input data validation
class SearchInput(BaseModel):
    query: str = Field(..., description="The search query to be executed")
    k: int = Field(3, description="The number of search results to retrieve")


# Class implementation for TavilySearch
class TavilySearchTool:
    def __init__(self, k: int = 3):
        """
        Initialize the TavilySearchTool with a specified number of results to return.
        """
        self.k = k
        self.web_search_tool = TavilySearchResults(k=self.k)

    def invoke(self, input_data: SearchInput):
        """
        Perform a web search using Tavily with the given query and retrieve results.
        """
        # Use the search query from the input_data
        results = self.web_search_tool.run(input_data.query)
        return results


# Example usage
if __name__ == "__main__":
    # Create an instance of SearchInput
    search_input = SearchInput(query="What is LangChain?", k=3)

    # Create an instance of TavilySearchTool
    search_tool = TavilySearchTool(k=search_input.k)

    # Perform the search and get results
    search_results = search_tool.invoke(search_input)

    # Print the search results
    print(f"Search Results: {search_results}")
