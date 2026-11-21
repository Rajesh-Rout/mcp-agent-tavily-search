import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

load_dotenv()

mcp = FastMCP("WebSearchServer")

tavily = TavilyClient(
    api_key = os.getenv("TAVILY_API_KEY")
)

@mcp.tool()
def web_seearch(query:str)->str:
    """
    Search web for information
    Args:
        query:Search query
    Returns:
        Search the web for the query
    """

    response = tavily.search(
        query = query,
        max_results = 5
    )

    results = []

    for item in response["results"]:
        results.append(
            f"""
            Title:{item["title"]}
            URL:{item["url"]}
            Content:{item["content"]}
            """
        )

    return  "\n".join(results)

# start the mcp server
if __name__=="__main__":
    mcp.run(transport = "stdio")