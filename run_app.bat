@echo off
echo ===================================================
echo   Entrepreneur Helper App - Auto Installer
echo ===================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo During installation, make sure to check "Add Python to PATH".
    echo.
    pause
    exit /b
)

echo [OK] Python is found.
echo.

:: 2. Upgrade pip and Install Requirements
echo [STEP 1/3] Installing Libraries (Flask, SQLite, etc)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install libraries. Check your internet connection.
    pause
    exit /b
)
echo.

:: 3. Seed Database
echo [STEP 2/3] Setting up Database (Real Data)...
python seed_db.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to setup database.
    pause
    exit /b
)
echo.

:: 4. Run App
echo [STEP 3/3] Starting Web Application...
echo.
echo ===================================================
echo   App is running!
echo   Open your browser and go to: http://127.0.0.1:5000
echo ===================================================
echo.
python app.py
pause
