#!/bin/bash
# ============================================================================
# RegressionLab - Setup Script for Unix/Mac
# ============================================================================
# This script sets up the development environment for RegressionLab
# ============================================================================

set -e  # Exit on error

echo ""
echo "===================================="
echo "   RegressionLab Setup (Unix/Mac)"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

# Check Python version is 3.11 or higher
python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" || {
    echo "ERROR: Python 3.11 or higher is required"
    exit 1
}
echo "      Python version OK"

echo ""
echo "[2/5] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "      Virtual environment already exists, skipping creation"
else
    python3 -m venv .venv
    echo "      Virtual environment created"
fi

echo ""
echo "[3/5] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[4/5] Upgrading pip..."
python -m pip install --upgrade pip

echo ""
echo "[5/6] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[6/6] Creating desktop shortcut..."

# Determine desktop path based on OS
if [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
elif [ -d "$HOME/desktop" ]; then
    DESKTOP_DIR="$HOME/desktop"
elif [ -d "$HOME/Escritorio" ]; then
    DESKTOP_DIR="$HOME/Escritorio"
else
    DESKTOP_DIR="$HOME"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$DESKTOP_DIR/RegressionLab.desktop"
ICON_PATH="$SCRIPT_DIR/images/RegressionLab_icon_low_res.ico"

# Create .desktop file
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=$(grep -E '^APP_VERSION=' "$SCRIPT_DIR/.env" | cut -d '=' -f2 | tr -d '"')
Type=Application
Name=RegressionLab
Comment=RegressionLab - Quick Launch
Exec=$SCRIPT_DIR/bin/run.sh
Path=$SCRIPT_DIR
Icon=$ICON_PATH
Terminal=true
Categories=Utility;Science;
EOF

# Make it executable
chmod +x "$DESKTOP_FILE"

if [ -f "$DESKTOP_FILE" ]; then
    echo "      Desktop shortcut created successfully at: $DESKTOP_FILE"
else
    echo "      Warning: Could not create desktop shortcut"
fi

echo ""
echo "===================================="
echo "   Setup Complete!"
echo "===================================="
echo ""
echo "To run RegressionLab:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Run the program: python main_program.py"
echo ""
echo "Or simply use: ./bin/run.sh"
echo "Or double-click the desktop shortcut: RegressionLab.desktop"
echo ""
echo "To configure the application:"
echo "  1. Copy .env.example to .env: cp .env.example .env"
echo "  2. Edit .env with your preferences"
echo ""
