#!/bin/bash
set -x

# Create a signal-cli directory in the current working directory
mkdir -p ./signal-cli
cd ./signal-cli || exit

# Define the URL to the latest release of signal-cli
SIGNAL_CLI_URL="https://github.com/AsamK/signal-cli/releases/download/v0.13.0/signal-cli-0.13.0.tar.gz"

# Check if curl is available
if ! command -v curl &>/dev/null; then
    echo "curl is required but not found. Please install curl and try again."
    exit  1
fi

# Check if tar is available
if ! command -v tar &>/dev/null; then
    echo "tar is required but not found. Please install tar and try again."
    exit  1
fi

# Download the latest release
echo "Downloading the latest signal-cli release..."
curl -L "$SIGNAL_CLI_URL" -o signal-cli.tar.gz

# Extract the downloaded file into the current directory
echo "Extracting the downloaded file..."
tar -xzf signal-cli.tar.gz --strip-components=1

# Remove the downloaded file
rm signal-cli.tar.gz

# Make the signal-cli executable
echo "Making signal-cli executable..."
chmod +x ./bin/signal-cli

# Verify the installation
echo "Verifying the installation..."
./bin/signal-cli --version

echo "signal-cli has been successfully installed in the ./signal-cli directory!"

# Prompt the user for the telephone number
read -p "Enter your Telephone Number (starting with +): " phoneNumber

# Check if the phone number starts with '+'
if [[ $phoneNumber != \+* ]]; then
    echo "Error: The telephone number must start with '+'."
    exit  1
fi

./bin/signal-cli/signal-cli -a "$phoneNumber" register
