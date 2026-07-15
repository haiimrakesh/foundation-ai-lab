---
name: run-ui
description: Run the React frontend application for the AI Agents chat UI.
arguments:
  - name: none
    description: No arguments are required.
---

This skill launches the React UI application for the repository using the configured package script.

Steps:
1. Ensure the React app package is available under the workspace app directory and the shell wrapper is present in the skill's Scripts folder.
2. Run the wrapper from the repository root with `./.github/skills/run-ui/Scripts/run-ui.sh`.
3. If the script is not executable, use `chmod +x ./.github/skills/run-ui/Scripts/run-ui.sh` first.

Use cases:
- Start the local React development server.
- Verify UI changes in the browser.
- Confirm the active agent chat interface is running.

Example prompts:
- "Run the React UI application."
- "Start the frontend chat app."
- "Launch the AI agent chat interface."

Notes:
- The wrapper locates the React app automatically from its own script path.
- If `node_modules` is missing, the script installs dependencies before starting the dev server.
- The script invokes `npm run start`, which is aliased to `vite`.
