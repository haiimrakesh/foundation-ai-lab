from __future__ import annotations

import os
from typing import Any


class LLMConfigurationError(RuntimeError):
    """Raised when required LLM configuration is missing or invalid."""


class LLMServiceError(RuntimeError):
    """Raised when the upstream LLM provider call fails."""


class LLMService:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        client: Any | None = None,
    ) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._client = client

        if self._client is not None:
            return

        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise LLMConfigurationError("OPENAI_API_KEY is not configured")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMConfigurationError(
                "OpenAI SDK is not installed. Install dependencies from requirements.txt"
            ) from exc

        self._client = OpenAI(api_key=key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    def generate(
        self,
        *,
        agent_id: str,
        agent_label: str,
        message: str,
        history: list[dict[str, Any]] | None = None,
    ) -> str:
        messages = self._build_messages(
            agent_id=agent_id,
            agent_label=agent_label,
            message=message,
            history=history,
        )

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
        except Exception as exc:
            raise LLMServiceError("OpenAI request failed") from exc

        content = response.choices[0].message.content
        if not content:
            raise LLMServiceError("OpenAI returned an empty response")
        return content

    def _build_messages(
        self,
        *,
        agent_id: str,
        agent_label: str,
        message: str,
        history: list[dict[str, Any]] | None,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are the Foundation AI Lab assistant operating as "
                    f"the {agent_label} ({agent_id}). Give concise, practical answers."
                ),
            }
        ]

        if history:
            for turn in history:
                normalized = self._normalize_history_turn(turn)
                if normalized is not None:
                    messages.append(normalized)

        messages.append({"role": "user", "content": message})
        return messages

    def _normalize_history_turn(self, turn: dict[str, Any]) -> dict[str, str] | None:
        role = turn.get("role")
        content = turn.get("content")

        if role in {"user", "assistant", "system"} and isinstance(content, str):
            return {"role": role, "content": content}

        sender = turn.get("sender")
        text = turn.get("text")
        if sender == "user" and isinstance(text, str):
            return {"role": "user", "content": text}
        if sender in {"agent", "assistant"} and isinstance(text, str):
            return {"role": "assistant", "content": text}

        return None