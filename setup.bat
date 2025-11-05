@echo off
REM PackCheck Setup Script for Windows

echo =====================================
echo PackCheck Installation Setup
echo =====================================

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed. Aborting.
    exit /b 1
)

REM Check Node.js version
echo Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is required but not installed. Aborting.
    exit /b 1
)

REM Check Tesseract OCR
echo Checking Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo Warning: Tesseract OCR not found. Please install it separately.
)

echo.
echo =====================================
echo Setting up Backend...
echo =====================================

REM Setup backend
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit backend\.env with your configuration
)

REM Create uploads directory
if not exist uploads mkdir uploads

echo Backend setup complete!

cd ..

echo.
echo =====================================
echo Setting up Frontend...
echo =====================================

REM Setup frontend
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

echo Frontend setup complete!

cd ..

echo.
echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo To start the application:
echo.
echo Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo The backend will run on http://localhost:5000
echo The frontend will run on http://localhost:3000
echo.

pause
