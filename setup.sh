#!/bin/bash

echo "🚀 Setting up Silver Breakout Analysis..."
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the analysis:"
echo "  source venv/bin/activate"
echo "  python run_analysis.py"
echo ""
echo "Or simply run:"
echo "  ./run_analysis.py"
echo "" 