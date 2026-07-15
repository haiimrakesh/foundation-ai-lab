from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    agent: Literal["rest", "keyword", "semantic", "tools", "mcp", "orchestration"]
    message: str
    history: list[dict] | None = None


class AgentChatRequest(BaseModel):
    message: str
    history: list[dict] | None = None


class ChatResponse(BaseModel):
    agent: str
    reply: str
    placeholder: bool
