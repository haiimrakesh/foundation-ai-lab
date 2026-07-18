---
name: get-setup
description: 'Bootstrap the Foundation AI Lab development environment. Use when: setting up the project for the first time, onboarding a new developer, recreating the Python virtual environment, installing dependencies from requirements.txt, or initializing the .env configuration file from .env.example.'
argument-hint: 'Optional: path to a custom requirements file or target directory'
---

# Setup Development Environment

## When to Use
- First-time project setup or onboarding
- Recreating a broken or missing Python virtual environment
- Installing or refreshing dependencies after `requirements.txt` changes
- Initialising the `.env` file from `.env.example`

## Procedure

1. **Run the setup script** — execute [./Scripts/setup-instructions.sh](./Scripts/setup-instructions.sh):
   ```bash
   bash .github/skills/get-setup/Scripts/setup-instructions.sh
   ```
   The script will:
   - Create a `venv/` virtual environment in the workspace root.
   - Activate the environment (handles Windows `msys`/`cygwin` and POSIX paths).
   - Install all packages listed in `requirements.txt`.
   - Copy `.env.example` → `.env` if `.env` does not already exist.
2. **Configure `.env`** — open the generated `.env` file and populate all required values (API keys, endpoints, etc.).
3. **Verify** — run a quick smoke-test to confirm the environment is healthy:
   ```bash
   source venv/Scripts/activate   # Windows (Git Bash / msys)
   # or
   source venv/bin/activate        # macOS / Linux
   python -c "import fastapi; print('OK')"
   ```

## Requirements
- Bash shell (Git Bash, WSL, or POSIX shell on macOS/Linux)
- Read/write access to the workspace root
- `.env.example` present at the workspace root for `.env` initialisation