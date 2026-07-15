import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Unified-Agent-Backend"))

from app.main import app


client = TestClient(app)


def test_placeholder_response_contract() -> None:
    response = client.post(
        "/api/chat",
        json={"agent": "orchestration", "message": "Summarize the plan", "history": []},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["agent"] == "orchestration"
    assert payload["placeholder"] is True
    assert "placeholder response" in payload["reply"].lower()
