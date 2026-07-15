import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import main
from app.llm import LLMConfigurationError, LLMServiceError


client = TestClient(main.app)


class FakeLLMService:
    def generate(
        self,
        *,
        agent_id: str,
        agent_label: str,
        message: str,
        history: list[dict] | None = None,
    ) -> str:
        return f"{agent_label}: {message}"


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_agents_returns_ids_labels_and_descriptions() -> None:
    response = client.get("/api/agents")

    assert response.status_code == 200
    payload = response.json()
    assert "agents" in payload
    assert len(payload["agents"]) >= 1

    first_agent = payload["agents"][0]
    assert "id" in first_agent
    assert "label" in first_agent
    assert "description" in first_agent


@pytest.mark.parametrize(
    ("agent", "expected_fragment"),
    [
        ("rest", "REST API Agent"),
        ("keyword", "Keyword Search Agent"),
        ("semantic", "Semantic Search Agent"),
        ("tools", "Tool Agent"),
        ("mcp", "MCP Agent"),
        ("orchestration", "Orchestration Agent"),
    ],
)
def test_agent_specific_endpoints_return_llm_response(
    monkeypatch: pytest.MonkeyPatch,
    agent: str,
    expected_fragment: str,
) -> None:
    monkeypatch.setattr(main, "get_llm_service", lambda: FakeLLMService())

    response = client.post(
        f"/api/agents/{agent}/chat",
        json={"message": "Hello there", "history": [{"role": "user", "content": "Hi"}]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["agent"] == agent
    assert payload["placeholder"] is False
    assert expected_fragment in payload["reply"]


def test_chat_endpoint_uses_same_llm_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "get_llm_service", lambda: FakeLLMService())

    response = client.post(
        "/api/chat",
        json={"agent": "rest", "message": "Test message", "history": []},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["agent"] == "rest"
    assert payload["placeholder"] is False
    assert "REST API Agent" in payload["reply"]


def test_unknown_agent_returns_404() -> None:
    response = client.post(
        "/api/agents/not-real/chat",
        json={"message": "Hi", "history": []},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Unknown agent"


def test_openai_failures_return_502(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailingService:
        def generate(self, **_: object) -> str:
            raise LLMServiceError("OpenAI request failed")

    monkeypatch.setattr(main, "get_llm_service", lambda: FailingService())

    response = client.post(
        "/api/chat",
        json={"agent": "rest", "message": "Will fail", "history": []},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "OpenAI request failed"


def test_missing_configuration_returns_500(monkeypatch: pytest.MonkeyPatch) -> None:
    class MisconfiguredService:
        def generate(self, **_: object) -> str:
            raise LLMConfigurationError("OPENAI_API_KEY is not configured")

    monkeypatch.setattr(main, "get_llm_service", lambda: MisconfiguredService())

    response = client.post(
        "/api/chat",
        json={"agent": "rest", "message": "Will fail", "history": []},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "OPENAI_API_KEY is not configured"
