#!/bin/bash

# Exit the script immediately if any command returns a non-zero (error) exit code
set -e

# activate the virtual environment if it exists
cd backend
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

# Set up the environment variables
export ENV=dev
echo "Setting environment to $ENV"

echo "🔍 Running tests..."
pytest --cov=src

cd ..

echo "🐳 Building Docker image..."
docker build -t sentinel-backend ./backend

echo "🚀 Running container..."
exec docker run --rm -p 8000:8000 -e ENV=dev -v $(pwd)/backend/serviceAccountKey.json:/app/serviceAccountKey.json -v $(pwd)/backend/.env:/app/.env sentinel-backend
