#!/bin/bash
# Streamlit launcher for RegressionLab (Unix/Linux/macOS)
# This script starts the Streamlit web application

set -e  # Exit on error

echo "Starting RegressionLab Streamlit Application..."
echo ""

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Run Streamlit application
streamlit run src/streamlit_app/app.py
