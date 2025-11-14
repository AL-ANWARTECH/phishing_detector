@echo off
echo ===========================================
echo Phishing Detection System Installation
echo ===========================================

REM Check if Python 3.8+ is installed
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

REM Check if Python version is 3.8 or higher
if %MAJOR% gtr 3 (
    goto version_ok
) else if %MAJOR% equ 3 (
    if %MINOR% geq 8 (
        goto version_ok
    )
)

echo Error: Python 3.8 or higher required. Current version: %PYTHON_VERSION%
pause
exit /b 1

:version_ok
echo ✓ Python %PYTHON_VERSION% found

REM Check if pip is installed
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed
    pause
    exit /b 1
)
echo ✓ pip found

REM Create virtual environment
echo Creating virtual environment...
python -m venv phishing_env

REM Activate virtual environment
echo Activating virtual environment...
call phishing_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist logs mkdir logs
if not exist models mkdir models
if not exist data mkdir data

REM Test the installation
echo Testing installation...
python -c "import flask, sklearn, requests" >nul 2>&1
if errorlevel 1 (
    echo Error: Dependency installation failed
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully

REM Create database
echo Initializing database...
python -c "from database import Database; db = Database(); print('Database initialized successfully')"

echo ===========================================
echo Installation completed successfully!
echo ===========================================
echo.
echo To start the application:
echo   1. Activate virtual environment: phishing_env\Scripts\activate.bat
echo   2. Start the web interface: python main.py
echo   3. Or use CLI: python cli.py analyze --file email.txt
echo.
echo Web interface will be available at: http://localhost:5000
echo API documentation: http://localhost:5000 (web interface)
echo.
echo For analytics dashboard (separate): python analytics_dashboard.py (port 5001)
echo ===========================================

pause