@echo off
REM Start FastAPI backend (Windows Batch)

echo 🏦 Starting BankSight AI Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Please run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Start backend with reload exclusions
echo Starting FastAPI server...
echo Excluding models/ and data/vector_db/ from file watching
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --reload-exclude "models/*" --reload-exclude "data/vector_db/*"
