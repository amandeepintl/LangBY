@echo off

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    msg * "Langby: Python is not installed. Download from python.org"
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        msg * "Langby: Failed to create virtual environment."
        exit /b 1
    )
)

:: Install dependencies silently
venv\Scripts\pip.exe install -r requirements.txt --quiet >nul 2>&1

:: Launch with pythonw (no console window)
start "" venv\Scripts\pythonw.exe langby.py
exit
