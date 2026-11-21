# WebSearch MCP Agent

A web search assistant built with **LangChain**, the **Model Context Protocol (MCP)** and **Tavily**. A custom MCP server exposes a `web_search` tool, and a LangChain agent (GPT-4o-mini) calls it to answer questions using live web results.

## How it works

```
User question -> LangChain agent (agent.py) -> MCP client (stdio)
                                                  |
                                                  v
                                 MCP server (mcp_server.py) -> Tavily Search API
```

1. `mcp_server.py` starts an MCP server (FastMCP) with one tool, `web_search`, which queries Tavily and returns the top 5 results.
2. `agent.py` launches the server as a subprocess over stdio and loads its tools with `langchain-mcp-adapters`.
3. The agent decides to call `web_search`, reads the results, and answers based only on them.

## Tech stack

- Python 3.12
- LangChain / `langchain-openai` (GPT-4o-mini)
- MCP (`mcp`, `langchain-mcp-adapters`)
- Tavily Search API
- uv (package manager)
- Docker (optional)

## Project structure

```
WebSearch_MCP_Agent/
├── agent.py            # LangChain agent + MCP client
├── mcp_server.py       # MCP server exposing the web_search tool
├── pyproject.toml      # Project dependencies (uv)
├── uv.lock             # Locked versions
├── requirements.txt    # Dependency list (pip-style)
├── Dockerfile          # Container build
├── .dockerignore
├── .env