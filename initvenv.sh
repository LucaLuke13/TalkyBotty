#!/bin/bash

# Define the name of the virtual environment
VENV_NAME="voicebot"

# Check if the virtual environment already exists
if [ ! -d "$VENV_NAME" ]; then
    # Create a new virtual environment
    echo "Creating a new virtual environment named $VENV_NAME..."
    python3 -m venv "$VENV_NAME"
else
    # Activate the existing virtual environment
    echo "Activating the existing virtual environment named $VENV_NAME..."
fi

# Source the virtual environment activation script
source "$VENV_NAME/bin/activate"