import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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
def test_agent_specific_endpoints_return_placeholder_response(agent: str, expected_fragment: str) -> None:
    response = client.post(
        f"/api/agents/{agent}/chat",
        json={"message": "Hello there", "history": []},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["agent"] == agent
    assert payload["placeholder"] is True
    assert expected_fragment in payload["reply"]
