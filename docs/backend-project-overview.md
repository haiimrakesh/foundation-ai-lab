# Backend Project Overview

## Purpose

The backend provides a FastAPI service that powers the chat UI and generates responses through the OpenAI SDK.

## Current endpoints

- GET /health returns a health check response.
- GET /api/agents lists the available agents.
- POST /api/chat accepts a shared chat request.
- POST /api/agents/{agent_id}/chat exposes dedicated routes per agent type.

## Development notes

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

Run the server with:

```bash
uvicorn app.main:app --reload --port 8000
```

Run this command from [Unified-Agent-Backend](Unified-Agent-Backend).

## Environment

Set these values in your local .env file (or exported environment):

- OPENAI_API_KEY: required for response generation.
- OPENAI_MODEL: optional, defaults to gpt-4o-mini.

If the OpenAI provider call fails, chat endpoints return HTTP 502.
If OPENAI_API_KEY is missing, chat endpoints return HTTP 500 with a configuration error.

## Scope

This is a synchronous MVP integration intended for simple backend responses.
Streaming, retry logic, token budgeting, and multi-provider routing are out of scope.
