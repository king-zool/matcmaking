#!/bin/bash

echo "AfCFTA Trade Matchmaker - Quick Deployment Setup"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AfCFTA Trade Matchmaker Platform"
fi

echo ""
echo "Deployment options:"
echo "1. Render - https://render.com"
echo "2. Railway - https://railway.app"
echo "3. PythonAnywhere - https://pythonanywhere.com"
echo "4. Heroku - https://heroku.com"
echo ""
echo "Configuration files created:"
echo "  - Procfile (for Heroku/Render)"
echo "  - runtime.txt (Python version)"
echo "  - render.yaml (Render configuration)"
echo "  - railway.json (Railway configuration)"
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository"
echo "2. Push this code: git remote add origin YOUR_REPO_URL"
echo "3. Follow DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "Admin credentials:"
echo "  Email: admin@afcfta.com"
echo "  Password: admin123"
echo "  (CHANGE IMMEDIATELY AFTER DEPLOYMENT)"
echo ""
