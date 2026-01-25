#!/bin/bash
# ============================================================================
# RegressionLab - Installation Script for Unix/Mac
# ============================================================================
# This script clones the repository and runs the setup automatically
# ============================================================================

set -e  # Exit on error

echo ""
echo "===================================="
echo "   RegressionLab Installation"
echo "===================================="
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    echo "Please install Git:"
    echo "  - Ubuntu/Debian: sudo apt-get install git"
    echo "  - macOS: git is included with Xcode Command Line Tools"
    echo "  - Or download from: https://git-scm.com/downloads"
    exit 1
fi

echo "[1/3] Git found:"
git --version

# Set repository URL
REPO_URL="https://github.com/DOKOS-TAYOS/RegressionLab.git"
REPO_NAME="regressionlab"

# Check if directory already exists
if [ -d "$REPO_NAME" ]; then
    echo ""
    echo "WARNING: Directory '$REPO_NAME' already exists"
    read -p "Do you want to remove it and clone again? (y/N): " OVERWRITE
    if [[ "$OVERWRITE" =~ ^[Yy]$ ]]; then
        echo "      Removing existing directory..."
        rm -rf "$REPO_NAME"
    else
        echo "      Using existing directory..."
        cd "$REPO_NAME"
        ./setup.sh
        exit 0
    fi
fi

echo ""
echo "[2/3] Cloning repository..."
if ! git clone "$REPO_URL"; then
    echo "ERROR: Failed to clone repository"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "      Repository cloned successfully"

# Change to repository directory
cd "$REPO_NAME" || {
    echo "ERROR: Failed to change to repository directory"
    exit 1
}

echo ""
echo "[3/3] Running setup..."
echo ""

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

echo ""
echo "===================================="
echo "   Installation Complete!"
echo "===================================="
echo ""
echo "The RegressionLab repository has been cloned and set up."
echo "You can now run the application from: $(pwd)"
echo ""
