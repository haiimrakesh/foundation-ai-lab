# Architecture Overview

## Overview

This repository contains a simple AI agent lab with two main pieces:

- a Vite + React frontend that provides the chat experience
- a FastAPI backend that exposes placeholder endpoints for each agent type

## Components

### Frontend

The frontend is a single-page React application that lets users:

- select an agent type
- send a message
- receive a backend response
- inspect the current payload preview

### Backend

The backend exposes:

- `/health` for health checks
- `/api/agents` for agent discovery
- `/api/chat` for a shared chat entry point
- `/api/agents/{agent_id}/chat` for agent-specific chat routes

## Request flow

1. The user selects an agent in the React UI.
2. The UI sends a POST request to the matching backend endpoint.
3. The FastAPI service returns a placeholder response that identifies the agent.
4. The frontend renders the reply in the conversation view.

## Future extension points

The current implementation uses placeholder responses so the interface contract is stable. Future work can replace the stub logic with:

- real model inference
- retrieval-augmented generation
- tool calling
- MCP integrations
- orchestrated multi-agent flows
