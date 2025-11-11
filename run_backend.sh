#!/bin/bash
# Start FastAPI backend

echo "🏦 Starting BankSight AI Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start backend
echo "Starting FastAPI server..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
