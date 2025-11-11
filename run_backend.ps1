# Start FastAPI backend (Windows PowerShell)

Write-Host "🏦 Starting BankSight AI Backend..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run: python -m venv venv" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Start backend with reload exclusions
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "Excluding models/ and data/vector_db/ from file watching" -ForegroundColor Gray
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --reload-exclude "models/*" --reload-exclude "data/vector_db/*"
