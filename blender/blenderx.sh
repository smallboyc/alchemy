echo "Launching Blender with Custom Tools..."

# Mac OS for the moment :D
BLENDER_BASE_PATH="/Applications/Blender.app/Contents/MacOS/blender"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLENDER_TOOLS_ROOT_PATH="$SCRIPT_DIR/main.py"

export ALCHEMY_ROOT="$SCRIPT_DIR"

"$BLENDER_BASE_PATH" --python "$BLENDER_TOOLS_ROOT_PATH"