from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from .llm import LLMConfigurationError, LLMService, LLMServiceError
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

AGENTS = {
    "rest": {
        "label": "REST API Agent",
        "description": "Inference via REST API backend",
    },
    "keyword": {
        "label": "Keyword Search Agent",
        "description": "Simple RAG with keyword search",
    },
    "semantic": {
        "label": "Semantic Search Agent",
        "description": "RAG with semantic search",
    },
    "tools": {
        "label": "Tool Agent",
        "description": "RAG with tool calling capability",
    },
    "mcp": {
        "label": "MCP Agent",
        "description": "RAG with MCP integration",
    },
    "orchestration": {
        "label": "Orchestration Agent",
        "description": "Multi-agent orchestration",
    },
}

_llm_service: LLMService | None = None


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/agents")
def list_agents() -> dict[str, list[dict[str, str]]]:
    return {
        "agents": [
            {
                "id": agent_id,
                "label": metadata["label"],
                "description": metadata["description"],
            }
            for agent_id, metadata in AGENTS.items()
        ]
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return build_response(request.agent, request.message, request.history)


@app.post("/api/agents/{agent_id}/chat", response_model=ChatResponse)
def agent_chat(agent_id: str, request: AgentChatRequest) -> ChatResponse:
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Unknown agent")
    return build_response(agent_id, request.message, request.history)


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def build_response(
    agent_id: str,
    message: str,
    history: list[dict] | None = None,
) -> ChatResponse:
    label = AGENTS[agent_id]["label"]
    try:
        reply = get_llm_service().generate(
            agent_id=agent_id,
            agent_label=label,
            message=message,
            history=history,
        )
    except LLMConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(agent=agent_id, reply=reply, placeholder=False)
