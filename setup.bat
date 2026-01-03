@echo off
REM This script automates the setup process for the Biological Pathway Mapping project.

echo --- Biological Pathway Mapping Setup ---

REM Step 1: Create a Python virtual environment
echo.
echo [1/3] Creating Python virtual environment in '.\.venv'...
python -m venv .venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment. Please ensure Python 3.9+ is installed.
    exit /b %errorlevel%
)

REM Step 2: Activate the virtual environment and install dependencies
echo.
echo [2/3] Activating virtual environment and installing dependencies from requirements.txt...

REM Activate for the current script session
call .venv\Scripts\activate.bat

REM Install packages
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies. Please check requirements.txt and your network connection.
    exit /b %errorlevel%
)

REM Step 3: Remind the user to install Ollama and pull the model
echo.
echo [3/3] Final steps: Please install Ollama and pull the required model.
echo --------------------------------------------------------------------
echo 1. Download and install Ollama from https://ollama.ai/
echo 2. After installation, run the following command in your terminal:
echo    ollama pull gemma3:1b
echo    (Optionally, for more powerful analysis, you can pull 'gpt:oss120b-cloud' if your system has sufficient resources.)
echo 3. Once the model is downloaded, you can run the application with:
echo    .venv\Scripts\activate.bat
echo    streamlit run streamlit_app.py
echo --------------------------------------------------------------------

echo.
echo Setup complete! Please follow the final steps above to run the application.
pause
