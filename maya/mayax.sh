echo "Launching Maya with Custom Tools..."

MAYA_BASE_PATH="/Applications/Autodesk/maya2025/Maya.app/Contents/bin/maya"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAYA_TOOLS_ROOT_PATH="$SCRIPT_DIR/main.py"

export ALCHEMY_ROOT="$SCRIPT_DIR"

"$MAYA_BASE_PATH" -command "python(\"exec(open('$MAYA_TOOLS_ROOT_PATH').read())\")"