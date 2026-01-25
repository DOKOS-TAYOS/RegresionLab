#!/bin/bash
# Open RegressionLab Documentation in Browser

echo "Opening RegressionLab documentation..."

# Detect OS and open with appropriate command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open build/html/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open build/html/index.html
else
    echo "Please open build/html/index.html manually in your browser."
fi
