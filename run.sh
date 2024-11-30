#!/bin/sh
set -e

# Fetch the most current version of the repository
echo "Fetching the latest version of the repository..."
git pull
echo "Repository updated successfully."

# Check for and create virtual environment if necessary
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    uv venv -p 3.12 .venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Install dependencies
uv pip install -U syftbox
uv pip install -r requirements.txt

# Activate the virtual environment
. .venv/bin/activate

# Run the application
echo "Running ring with $(python3 --version) at '$(which python3)'"
python3 main.py

# Deactivate the virtual environment
deactivate