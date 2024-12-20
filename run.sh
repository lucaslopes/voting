#!/bin/sh

# Ensure NVM is loaded
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  . "$NVM_DIR/nvm.sh"  # This loads nvm
fi
if [ -s "$NVM_DIR/bash_completion" ]; then
  . "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
fi

# Source the appropriate shell configuration file
source_shell_config() {
  if [ -n "$ZSH_VERSION" ]; then
    # Running in Zsh
    if [ -f "$HOME/.zshrc" ]; then
      source "$HOME/.zshrc"
    else
      echo "Warning: ~/.zshrc not found. Skipping."
    fi
  elif [ -n "$BASH_VERSION" ]; then
    # Running in Bash
    if [ -f "$HOME/.bashrc" ]; then
      source "$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
      source "$HOME/.bash_profile"
    else
      echo "Warning: Neither ~/.bashrc nor ~/.bash_profile found. Skipping."
    fi
  else
    echo "Unsupported shell. Please ensure you're using Bash or Zsh."
    exit 1
  fi
}

# Ensure the script runs in the appropriate shell
if [ "$SHELL" = "/bin/zsh" ]; then
  echo "Running in Zsh."
elif [ "$SHELL" = "/bin/bash" ]; then
  echo "Running in Bash."
else
  exec /bin/zsh "$0"
fi

# Fetch the most current version of the repository
echo "Fetching the latest version of the repository..."
git pull --quiet
if [ $? -eq 0 ]; then
  echo "Repository updated successfully."
  if command -v npm >/dev/null 2>&1 || [ ! -f dist/index.html ]; then
    echo "Setting up Node environment..."
    curl -s -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
    source_shell_config
    nvm install --lts >/dev/null 2>&1
    npm install --force --silent >/dev/null 2>&1
    npm run format --silent
    npm run build --silent
    echo "Node environment setup complete."
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
  uv venv -p 3.12 .venv >/dev/null 2>&1
  echo "Virtual environment created successfully."
else
  echo "Virtual environment already exists."
fi

# Activate the virtual environment
. .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
uv pip install -U syftbox >/dev/null 2>&1
uv pip install -r api/requirements.txt >/dev/null 2>&1
echo "Python dependencies installed."

# Run the application
echo "Running ring with $(python3 --version) at '$(which python3)'"
python3 api/main.py

# Deactivate the virtual environment
deactivate