import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
import sys
from pathlib import Path
import asyncio

load_dotenv()

server_path = Path("mcp_server.py").resolve()

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.1
)

client = MultiServerMCPClient(
    {
        "web_search":{
            "transport":"stdio",
            "command":sys.executable,
            "args":[str(server_path)]

        }
    }
)

SYSTEM_PROMPT = (
    "You are a web search assistant. "
    "Always use the web_search tool to answer the user's question. "
    "Base your answer only on the search results. "
    "If the results don't contain the answer, say you could not find it."
)
# create the main fuction
async def main():

    # get the tools from mcp server
    tools = await client.get_tools()

    print("Available MCP tools:")
    for tool in tools:
        print(tool.name)

    # create a AI agent with mcp tools
    agent = create_agent(
        model = llm,
        tools = tools,
        system_prompt = SYSTEM_PROMPT

    )

    query = "What are the latest developments in Agentic AI?"

    response = await agent.ainvoke(
        {
            "messages":{"role":"user","content":query}
        }
    )

    print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())