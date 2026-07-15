import os
from .eval_template import mock_run_prompt, assert_response_contains


def test_simple_prompt_echo():
    prompt = "Summarize: Hello world"
    inputs = {"sample": "data"}
    resp = mock_run_prompt(prompt, inputs)
    assert_response_contains(resp, "Summarize")


def test_io_contract():
    prompt = "Return JSON with keys a and b"
    resp = mock_run_prompt(prompt, {})
    assert "text" in resp
