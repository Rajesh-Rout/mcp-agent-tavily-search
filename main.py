from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import create_web_agent


# Startup and shutdown lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create agent when API starts
    app.state.agent = await create_web_agent()

    print("Agent initialized successfully")

    yield

    print("API shutting down")


app = FastAPI(
    title="Web Search AI Agent",
    description="AI agent connected to a Web Search MCP Server",
    version="1.0",
    lifespan=lifespan
)


# Request schema
class AskRequest(BaseModel):
    question: str


# Response schema
class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
async def home():
    return {
        "message": "Web Search AI Agent is running"
    }


@app.post("/ask", response_model=AskResponse)
async def ask_agent(request: AskRequest):

    try:
        # Get agent from FastAPI application state
        agent = app.state.agent

        # Send user question to agent
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.question
                    }
                ]
            }
        )

        # Extract final AI response
        answer = result["messages"][-1].content

        return AskResponse(
            question=request.question,
            answer=answer
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )