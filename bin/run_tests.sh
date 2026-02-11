#!/bin/bash
# Run all tests for RegressionLab project

set -e  # Exit on error

# Change to project root directory (parent of bin)
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "Running RegressionLab tests..."
python tests/run_tests.py
