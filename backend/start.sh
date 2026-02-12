#!/bin/bash
# Render Startup Script for Agentic AI Hiring Platform

echo "🚀 Starting Agentic AI Hiring Platform..."

# Print Python version
echo "Python version:"
python --version

# Print installed packages
echo "Installed packages:"
pip list

# Run database migrations (if needed)
# Uncomment if you're using Alembic migrations
# echo "Running database migrations..."
# alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
