---
name: run-full-stack
description: Run the FastAPI backend and React frontend simultaneously for the Foundation AI Lab workspace.
arguments:
  - name: none
    description: No arguments are required.
---

This skill starts the backend API and the chat frontend together so they can be used side by side during local development.

Steps:
1. Ensure the repository contains both the Unified-Agent-Backend and Unified-Chat-Application directories.
2. Run the wrapper from the repository root with `./.github/skills/run-full-stack/Scripts/run-full-stack.sh`.
3. If the script is not executable, use `chmod +x ./.github/skills/run-full-stack/Scripts/run-full-stack.sh` first.
4. The backend will be available at `http://127.0.0.1:8000` and the frontend at `http://127.0.0.1:5173`.

Use cases:
- Start both the backend and UI together.
- Test end-to-end chat flows locally.
- Verify API and UI integration in one workflow.

Example prompts:
- "Run the full-stack app."
- "Start the backend and frontend together."
- "Launch the AI lab app locally."

Notes:
- The launcher installs frontend dependencies if needed and uses the current Python requirements for the backend.
- The script runs both services in the same terminal session and stops them together when interrupted.
