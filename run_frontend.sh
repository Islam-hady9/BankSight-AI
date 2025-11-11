#!/bin/bash
# Start Streamlit frontend

echo "🏦 Starting BankSight AI Frontend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start frontend
echo "Starting Streamlit app..."
streamlit run frontend/app.py
