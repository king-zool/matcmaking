@echo off
REM AfCFTA Trade Matchmaker - Quick Setup Script for Windows
REM This script sets up and runs the MVP platform

echo 🌍 AfCFTA Trade Matchmaker MVP Setup
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies. Please check your Python/pip setup.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Create sample data
echo 🗂️  Creating sample AfCFTA trade data...
python create_sample_data.py

if errorlevel 1 (
    echo ❌ Failed to create sample data.
    pause
    exit /b 1
)

echo ✅ Sample data created successfully
echo.

REM Start the application
echo 🚀 Starting AfCFTA Trade Matchmaker...
echo 📍 The application will be available at: http://localhost:5000
echo.
echo 🔑 Sample login credentials:
echo    Exporter: africagrains@example.com / password123
echo    Importer: foodimport@example.com / password123
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause