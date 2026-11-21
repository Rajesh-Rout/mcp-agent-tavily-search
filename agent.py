import os
from pathlib import Path

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient


# Get the absolute path of MCP server
server_path = Path("web_search_mcp.py").resolve()


# MCP Client
client = MultiServerMCPClient(
    {
        "web_search_server": {
            "transport": "stdio",
            "command": "python",
            "args": [str(server_path)]
        }
    }
)


# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


async def create_web_agent():

    # Retrieve tools from MCP server
    tools = await client.get_tools()

    print("MCP tools loaded:")
    for tool in tools:
        print(tool.name)

    # Create agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are a web research AI assistant.

        Use the web_search tool for current, recent,
        or internet-based information.

        When you search:
        1. Analyze the search results.
        2. Prefer reliable information.
        3. Do not invent facts.
        4. Give a clear and structured answer.
        """
    )

    return agent