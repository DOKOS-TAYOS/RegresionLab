#!/bin/bash
# Open RegressionLab Documentation in Browser
# Uses script directory so it works from any CWD.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCINDEX="${SCRIPT_DIR}/build/html/index.html"

echo "Opening RegressionLab documentation..."
if [[ -f "$DOCINDEX" ]]; then
    case "$OSTYPE" in
        darwin*)
            open "$DOCINDEX"
            ;;
        linux-gnu*)
            xdg-open "$DOCINDEX"
            ;;
        *)
            echo "Please open the following file in your browser:"
            echo "$DOCINDEX"
            ;;
    esac
else
    echo "ERROR: Documentation not found."
    echo "Looked at: $DOCINDEX"
    echo ""
    echo "Build the docs from this folder first: sphinx-docs/build_docs.sh"
    exit 1
fi
