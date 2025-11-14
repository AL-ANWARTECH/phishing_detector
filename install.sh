#!/bin/bash

# Phishing Detection System Installation Script
echo "==========================================="
echo "Phishing Detection System Installation"
echo "==========================================="

# Check if Python 3.8+ is installed
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -n1)
    if (( $(echo "$PYTHON_VERSION >= 3.8" | bc -l) )); then
        echo "✓ Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    else
        echo "✗ Python 3.8 or higher required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "✗ Python3 not found"
    exit 1
fi

# Check if pip is installed
echo "Checking pip..."
if command -v pip &> /dev/null; then
    echo "✓ pip found"
elif command -v pip3 &> /dev/null; then
    echo "✓ pip3 found"
    PIP_CMD="pip3"
else
    echo "✗ pip not found"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv phishing_env

# Activate virtual environment
echo "Activating virtual environment..."
source phishing_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs models data

# Test the installation
echo "Testing installation..."
if python -c "import flask, sklearn, requests" 2>/dev/null; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Dependency installation failed"
    exit 1
fi

# Create database
echo "Initializing database..."
python -c "
from database import Database
db = Database()
print('Database initialized successfully')
"

echo "==========================================="
echo "Installation completed successfully!"
echo "==========================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source phishing_env/bin/activate"
echo "  2. Start the web interface: python main.py"
echo "  3. Or use CLI: python cli.py analyze --file email.txt"
echo ""
echo "Web interface will be available at: http://localhost:5000"
echo "API documentation: http://localhost:5000 (web interface)"
echo ""
echo "For analytics dashboard (separate): python analytics_dashboard.py (port 5001)"
echo "==========================================="