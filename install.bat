@echo off
title AutomatePortal - Professional Installer
color 0B
echo.
echo  ==============================================================
echo     _   _   _ _____ ___  __  __    _  _____ _____
echo    / \ | | | |_   _/ _ \|  \/  |  / \|_   _| ____|
echo   / _ \| | | | | || | | | |\/| | / _ \ | | |  _|
echo  / ___ \ |_| | | || |_| | |  | |/ ___ \| | | |___
echo /_/   \_\___/  |_| \___/|_|  |_/_/   \_\_| |_____|
echo  ____   ___  ____ _____  _    _
echo |  _ \ / _ \|  _ \_   _|/ \  | |
echo | |_) | | | | |_) || | / _ \ | |
echo |  __/| |_| |  _ < | |/ ___ \| |___
echo |_|    \___/|_| \_\|_/_/   \_\_____|
echo.
echo  ==============================================================
echo   AI-Powered Browser Automation Platform
echo   Professional Installation
echo  ==============================================================
echo.

:: Check for admin rights
net session >/dev/null 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Running without administrator privileges.
    echo           Some features may require elevated permissions.
    echo.
)

:: Check Python installation
echo [1/7] Checking Python installation...
python --version >/dev/null 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Please install Python 3.9+ from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo         Python %PYVER% found.
echo.

:: Create virtual environment
echo [2/7] Creating isolated virtual environment...
if exist "venv" (
    echo         Virtual environment already exists. Skipping.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         Virtual environment created.
)
echo.

:: Activate virtual environment and install dependencies
echo [3/7] Installing dependencies (this may take a few minutes)...
call venv\Scripts\activate.bat
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements_v2.txt 2>&1 | findstr /i "error"
if %errorlevel% equ 0 (
    echo [WARNING] Some packages had errors. The app may still work.
) else (
    echo         All dependencies installed successfully.
)
pip install keyrings.alt >/dev/null 2>&1
echo.

:: Initialize database
echo [4/7] Initializing database...
python -c "from database import init_database; init_database()" 2>&1
echo.

:: Create data directories
echo [5/7] Creating application directories...
if not exist "data" mkdir data
if not exist "data\downloads" mkdir data\downloads
if not exist "data\logs" mkdir data\logs
if not exist "data\backups" mkdir data\backups
echo         Application directories created.
echo.

:: Setup environment file
echo [6/7] Configuring environment...
if not exist ".env" (
    copy .env.example .env >/dev/null 2>&1
    if not exist ".env" (
        echo FLASK_SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%> .env
        echo NOVA_ACT_API_KEY=>> .env
    )
    echo         Environment file created. You will configure your API key on first launch.
) else (
    echo         Environment file already exists. Skipping.
)
echo.

:: Create desktop shortcut
echo [7/7] Creating launcher shortcuts...
(
echo @echo off
echo title AutomatePortal
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo echo.
echo echo  Starting AutomatePortal...
echo echo  Dashboard will open at: http://localhost:5000
echo echo  Press Ctrl+C to stop the server.
echo echo.
echo timeout /t 2 /nobreak ^>/dev/null
echo start http://localhost:5000
echo python agent_dashboard_v2.py
) > "Start AutomatePortal.bat"
echo         Launcher created: "Start AutomatePortal.bat"
echo.

echo  ==============================================================
echo   INSTALLATION COMPLETE
echo  ==============================================================
echo.
echo   To start AutomatePortal:
echo     Double-click "Start AutomatePortal.bat"
echo.
echo   First-time setup:
echo     1. Open http://localhost:5000 in your browser
echo     2. Complete the setup wizard (set your password + API key)
echo.
echo   Default credentials (CHANGE IMMEDIATELY):
echo     Username: admin
echo     Password: admin123
echo.
echo  ==============================================================
echo.
pause
