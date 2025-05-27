#!/bin/bash
set -e

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies with docs extras
pip install -e ".[docs]"

# Create initial build to verify setup
mkdocs build

echo "Setup complete! You can now run 'source .venv/bin/activate' to activate the virtual environment"
echo "Then use 'mkdocs serve' to preview the documentation locally"
