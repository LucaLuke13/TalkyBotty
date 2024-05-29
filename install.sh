#!/bin/bash

# Function to execute a script and check for errors
execute_script() {
    echo "Running $1..."
    bash "$1"
    if [ $? -ne  0 ]; then
        echo "Error: Failed to run $1."
        exit  1
    fi
}

# Execute the scripts in sequence
execute_script init_signal-cli.sh
execute_script initvenv.sh
execute_script init_whisper.cpp.sh

echo "All scripts executed successfully."
