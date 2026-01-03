#!/bin/bash

# This script automates the setup process for the Biological Pathway Mapping project.

echo "--- Biological Pathway Mapping Setup ---"

# Step 1: Create a Python virtual environment
echo "\n[1/3] Creating Python virtual environment in './.venv'..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment. Please ensure Python 3.9+ is installed."
    exit 1
fi

# Step 2: Activate the virtual environment and install dependencies
echo "\n[2/3] Activating virtual environment and installing dependencies from requirements.txt..."

# Activate for the current script session
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies. Please check requirements.txt and your network connection."
    exit 1
fi

# Step 3: Remind the user to install Ollama and pull the model
echo "\n[3/3] Final steps: Please install Ollama and pull the required model."
echo "--------------------------------------------------------------------"
echo "1. Download and install Ollama from https://ollama.ai/"
echo "2. After installation, run the following command in your terminal:"
echo "   ollama pull gemma3:1b"
echo "   (Optionally, for more powerful analysis, you can pull 'gpt:oss120b-cloud' if your system has sufficient resources.)"
echo "3. Once the model is downloaded, you can run the application with:"
echo "   source .venv/bin/activate"
echo "   streamlit run streamlit_app.py"
echo "--------------------------------------------------------------------"

echo "\nSetup complete! Please follow the final steps above to run the application."
