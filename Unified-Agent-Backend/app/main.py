from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import AgentChatRequest, ChatRequest, ChatResponse

app = FastAPI(title="Foundation AI Lab Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENT_LABELS = {
    "rest": "REST API Agent",
    "keyword": "Keyword Search Agent",
    "semantic": "Semantic Search Agent",
    "tools": "Tool Agent",
    "mcp": "MCP Agent",
    "orchestration": "Orchestration Agent",
}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/agents")
def list_agents() -> dict[str, list[dict[str, str]]]:
    return {
        "agents": [
            {"id": agent_id, "label": label}
            for agent_id, label in AGENT_LABELS.items()
        ]
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return build_response(request.agent, request.message)


@app.post("/api/agents/{agent_id}/chat", response_model=ChatResponse)
def agent_chat(agent_id: str, request: AgentChatRequest) -> ChatResponse:
    if agent_id not in AGENT_LABELS:
        raise HTTPException(status_code=404, detail="Unknown agent")
    return build_response(agent_id, request.message)


def build_response(agent_id: str, message: str) -> ChatResponse:
    label = AGENT_LABELS[agent_id]
    reply = (
        f"{label} placeholder response: I received '{message}'. "
        "This backend is wired for future RAG and tool integrations."
    )
    return ChatResponse(agent=agent_id, reply=reply, placeholder=True)
