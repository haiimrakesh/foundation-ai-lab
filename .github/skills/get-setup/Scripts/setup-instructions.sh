#!/bin/bash
set -euo pipefail

is_windows_shell() {
    [[ "$OSTYPE" == msys* || "$OSTYPE" == cygwin* ]]
}

# Resolve an available Python command.
python_cmd=""
if command -v python >/dev/null 2>&1; then
    python_cmd="python"
elif command -v python3 >/dev/null 2>&1; then
    python_cmd="python3"
fi

# Check if Python is installed and install it if not.
if [[ -z "$python_cmd" ]]; then
    echo "Python is not installed. Installing Python..."
    if [[ "$OSTYPE" == linux-gnu* ]]; then
        sudo apt update
        sudo apt install -y python3 python3-venv python3-pip
        python_cmd="python3"
    elif [[ "$OSTYPE" == darwin* ]]; then
        brew install python
        python_cmd="python3"
    elif is_windows_shell; then
        echo "Please install Python manually from https://www.python.org/downloads/windows/ and ensure it's added to your PATH."
        exit 1
    else
        echo "Unsupported OS. Please install Python manually."
        exit 1
    fi
else
    echo "Python is already installed."
fi

# Check if python environment is already set up
if [ -d "venv" ]; then
    echo "Python virtual environment already exists. Skipping creation."
else    
    # Create a Python environment
    echo "Creating Python virtual environment..."
    "$python_cmd" -m venv venv
fi

# Check if venv is activated
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    echo "Python virtual environment is already activated."
else
    echo "Activating Python virtual environment..."
    # Activate the virtual environment, picking whichever activate script
    # actually exists (layout depends on the Python that created the venv,
    # not just the current shell type).
    if [ -f "venv/Scripts/activate" ]; then
        . venv/Scripts/activate
    elif [ -f "venv/bin/activate" ]; then
        . venv/bin/activate
    else
        echo "Error: could not find an activate script under venv/Scripts or venv/bin."
        exit 1
    fi
fi

# Check if pip is available for the selected Python interpreter.
if ! "$python_cmd" -m pip --version >/dev/null 2>&1; then
    echo "pip is not installed. Installing pip..."
    if [[ "$OSTYPE" == linux-gnu* ]] && command -v apt >/dev/null 2>&1; then
        # On Debian/Ubuntu, ensurepip is often stripped from the system Python,
        # so install pip via the distro package manager instead.
        sudo apt update
        sudo apt install -y python3-pip python3-venv
    elif [[ "$OSTYPE" == darwin* ]] && command -v brew >/dev/null 2>&1; then
        brew install python
    else
        "$python_cmd" -m ensurepip --upgrade
    fi

    if ! "$python_cmd" -m pip --version >/dev/null 2>&1; then
        echo "Error: pip could not be installed automatically. Please install pip manually for $python_cmd and re-run this script."
        exit 1
    fi
else
    echo "pip is already installed."
fi

# Install requirements
echo "Installing requirements from requirements.txt..."
"$python_cmd" -m pip install -r requirements.txt

# Create .env file from .env.example
if [ -f .env ]; then
    echo ".env file already exists. Skipping creation."
elif [ -f .env.example ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created successfully. Please update it with your configuration values."
else
    echo "Warning: .env.example file not found."
fi

echo "Setup complete!"
