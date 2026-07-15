import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.llm import LLMConfigurationError, LLMService, LLMServiceError


class _FakeMessage:
    def __init__(self, content: str | None) -> None:
        self.content = content


class _FakeChoice:
    def __init__(self, content: str | None) -> None:
        self.message = _FakeMessage(content)


class _FakeResponse:
    def __init__(self, content: str | None) -> None:
        self.choices = [_FakeChoice(content)]


class _FakeCompletions:
    def __init__(self, content: str | None = "ok", should_raise: bool = False) -> None:
        self.content = content
        self.should_raise = should_raise
        self.last_payload: dict | None = None

    def create(self, *, model: str, messages: list[dict[str, str]]) -> _FakeResponse:
        self.last_payload = {"model": model, "messages": messages}
        if self.should_raise:
            raise RuntimeError("boom")
        return _FakeResponse(self.content)


class _FakeChat:
    def __init__(self, completions: _FakeCompletions) -> None:
        self.completions = completions


class _FakeClient:
    def __init__(self, completions: _FakeCompletions) -> None:
        self.chat = _FakeChat(completions)


def test_requires_api_key_when_no_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(LLMConfigurationError, match="OPENAI_API_KEY"):
        LLMService(client=None)


def test_generate_builds_messages_with_history() -> None:
    completions = _FakeCompletions(content="Generated reply")
    service = LLMService(model="gpt-4o-mini", client=_FakeClient(completions))

    output = service.generate(
        agent_id="rest",
        agent_label="REST API Agent",
        message="How do I call endpoint X?",
        history=[
            {"role": "user", "content": "Hello"},
            {"sender": "assistant", "text": "Hi, how can I help?"},
            {"ignored": "value"},
        ],
    )

    assert output == "Generated reply"
    assert completions.last_payload is not None
    assert completions.last_payload["model"] == "gpt-4o-mini"
    messages = completions.last_payload["messages"]
    assert messages[0]["role"] == "system"
    assert "REST API Agent" in messages[0]["content"]
    assert messages[1] == {"role": "user", "content": "Hello"}
    assert messages[2] == {"role": "assistant", "content": "Hi, how can I help?"}
    assert messages[-1] == {"role": "user", "content": "How do I call endpoint X?"}


def test_generate_maps_provider_errors() -> None:
    completions = _FakeCompletions(should_raise=True)
    service = LLMService(client=_FakeClient(completions))

    with pytest.raises(LLMServiceError, match="OpenAI request failed"):
        service.generate(
            agent_id="rest",
            agent_label="REST API Agent",
            message="Hello",
            history=[],
        )


def test_generate_rejects_empty_provider_response() -> None:
    completions = _FakeCompletions(content=None)
    service = LLMService(client=_FakeClient(completions))

    with pytest.raises(LLMServiceError, match="empty response"):
        service.generate(
            agent_id="rest",
            agent_label="REST API Agent",
            message="Hello",
            history=[],
        )