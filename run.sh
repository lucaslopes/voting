#!/bin/sh
set -e

# Fetch the most current version of the repository
echo "Fetching the latest version of the repository..."
git pull --quiet
if [ $? -eq 0 ]; then
    echo "Repository updated successfully."
    if command -v npm >/dev/null 2>&1 || [ ! -f dist/index.html ]; then
        npm install --force && npm run format && npm run build
    else
        echo "npm is not installed. Please install npm to proceed."
        exit 1
    fi
else
    echo "Repository is already up to date."
fi

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
uv pip install -r api/requirements.txt

# Activate the virtual environment
. .venv/bin/activate

# Run the application
echo "Running ring with $(python3 --version) at '$(which python3)'"
python3 api/main.py

# Deactivate the virtual environment
deactivate