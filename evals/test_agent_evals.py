import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Unified-Agent-Backend"))

from app import main


client = TestClient(main.app)


class FakeLLMService:
    def generate(self, **_: object) -> str:
        return "Orchestration Agent: Summarized plan."


def test_llm_response_contract(monkeypatch) -> None:
    monkeypatch.setattr(main, "get_llm_service", lambda: FakeLLMService())

    response = client.post(
        "/api/chat",
        json={"agent": "orchestration", "message": "Summarize the plan", "history": []},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["agent"] == "orchestration"
    assert payload["placeholder"] is False
    assert "summarized plan" in payload["reply"].lower()
