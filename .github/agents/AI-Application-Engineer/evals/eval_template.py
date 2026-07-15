"""Evaluation helper templates for agent outputs.

Provide lightweight utilities to load prompts, run the agent logic (mocked), and assert expected outputs.
"""
from typing import Any, Dict

def mock_run_prompt(prompt: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Replace with real runner or a mock that simulates model responses."""
    # Simple deterministic mock for tests
    return {"text": f"ECHO: {prompt[:50]}", "metadata": {"inputs": inputs}}

def assert_response_contains(resp: Dict[str, Any], substr: str) -> None:
    assert substr in resp.get("text", ""), f"Response missing '{substr}'"
