@echo off
REM Start script for AI Paraphraser Web Interface (Windows)

echo ==========================================
echo   AI Paraphraser - Web Interface
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Warning: Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Warning: Dependencies not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed
    echo.
)

REM Start the web server
echo ==========================================
echo   Starting Web Server...
echo ==========================================
echo.

REM Use port from argument or default to 8080
if "%1"=="" (
    set PORT=8080
) else (
    set PORT=%1
)
python app.py %PORT%

pause
