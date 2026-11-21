import os
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

mcp = FastMCP("WebSearchServer")

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

@mcp.tool()
def web_search(query: str) -> str:
    """Search the internet for the given query."""

    response = tavily.search(
        query=query,
        max_results=5
    )

    results = []

    for item in response.get("results", []):
        results.append(
            f"""
            Title: {item.get('title')}
            URL: {item.get('url')}
            Content: {item.get('content')}
            """
        )

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run(transport="stdio")