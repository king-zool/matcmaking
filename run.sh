#!/bin/bash

# AfCFTA Trade Matchmaker - Quick Setup Script
# This script sets up and runs the MVP platform

echo "🌍 AfCFTA Trade Matchmaker MVP Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python/pip setup."
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Create sample data
echo "🗂️  Creating sample AfCFTA trade data..."
python3 create_sample_data.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to create sample data."
    exit 1
fi

echo "✅ Sample data created successfully"
echo ""

# Start the application
echo "🚀 Starting AfCFTA Trade Matchmaker..."
echo "📍 The application will be available at: http://localhost:5000"
echo ""
echo "🔑 Sample login credentials:"
echo "   Exporter: africagrains@example.com / password123"
echo "   Importer: foodimport@example.com / password123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py