#!/bin/bash

# Script to run the FastAPI backend for Foundation AI Lab
# This script uses the setup-instructions.sh to ensure all dependencies are installed

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

echo "Foundation AI Lab - Backend Server"
echo "===================================="
echo ""

# Step 1: Run setup if venv doesn't exist or dependencies are missing
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Step 1: Setting up development environment..."
    bash "$PROJECT_ROOT/.github/skills/get-setup/Scripts/setup-instructions.sh"
else
    echo "Step 1: Python environment already exists. Skipping setup."
fi

# Step 2: Locate the venv's Python interpreter directly.
# We avoid "source venv/.../activate" + bare "python"/"python3" because on
# Windows venvs there is no "python3" executable, and when this script is
# invoked via WSL's bash (which can happen even from a Windows PowerShell
# terminal since "bash" resolves to WSL's bash.exe), a plain "python"/"python3"
# resolves to WSL's own interpreter instead of the project's venv - causing
# "ModuleNotFoundError" even though the packages are installed.
echo "Step 2: Locating virtual environment interpreter..."
if [ -f "$PROJECT_ROOT/venv/Scripts/python.exe" ]; then
    # Windows-style venv. This also works correctly under WSL via interop.
    PYTHON_BIN="$PROJECT_ROOT/venv/Scripts/python.exe"
elif [ -f "$PROJECT_ROOT/venv/bin/python" ]; then
    PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"
else
    echo "Error: Could not find a Python interpreter in the venv." >&2
    exit 1
fi

# Step 3: Verify required packages
echo "Step 3: Verifying required packages..."
"$PYTHON_BIN" -c "import fastapi; import uvicorn; print('✓ Dependencies available')"

echo ""
echo "Step 4: Starting FastAPI backend server..."
echo "-------------------------------------------"
echo "Server will be available at: http://localhost:8000"
echo "API docs available at: http://localhost:8000/docs"
echo "ReDoc available at: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Step 5: Start the FastAPI backend
cd "$PROJECT_ROOT"
"$PYTHON_BIN" -m uvicorn Unified-Agent-Backend.app.main:app \
    --reload \
    --host 127.0.0.1 \
    --port 8000 \
    --log-level info
