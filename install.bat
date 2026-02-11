@echo off
echo.
echo ========================================
echo   WhisprByTheo Windows Installer
echo ========================================
echo.

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python from python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Try running: pip install pywebview pyaudio keyboard pyperclip requests
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation complete!
echo ========================================
echo.
echo To run WhisprByTheo:
echo   python whispr.py
echo.
echo On first run, you'll be asked for your OpenAI API key.
echo Get one at: https://platform.openai.com/api-keys
echo.
echo Default hotkey: F8 (hold to record, release to transcribe)
echo.
pause
