# Backend Project Overview

## Purpose

The backend provides a simple FastAPI service that powers the chat UI with placeholder responses for each agent type.

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
uvicorn backend.app.main:app --reload --port 8000
```
