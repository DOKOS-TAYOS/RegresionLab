#!/bin/bash
# Run all tests for RegressionLab project

set -e  # Exit on error

echo "Running RegressionLab tests..."
python tests/run_tests.py
