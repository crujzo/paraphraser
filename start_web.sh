#!/bin/bash

# Start script for AI Paraphraser Web Interface

echo "=========================================="
echo "  AI Paraphraser - Web Interface"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Start the web server
echo "=========================================="
echo "  Starting Web Server..."
echo "=========================================="
echo ""

# Use port from argument or default to 8080
PORT=${1:-8080}
python app.py $PORT
