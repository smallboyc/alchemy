import os
import sys
import maya.cmds as cmds

# TODO:
# - Install the Mayapy vs code extension
# - (optional) In order to have autocomplete working I had to change "python.autoComplete.extraPaths" in the json settings for "python.analysis.extraPaths"
# add userSetup.mel with "commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;" to run python script in real time.

TOOLS_ROOT = os.environ.get("ALCHEMY_ROOT")

if not TOOLS_ROOT:
    raise RuntimeError("ALCHEMY_ROOT environment variable is not set")

sys.path.append(TOOLS_ROOT)

# Shelf
SHELF_NAME = "Alchemy"


def create_shelf():
    if cmds.shelfLayout(SHELF_NAME, exists=True):
        cmds.deleteUI(SHELF_NAME)

    cmds.shelfLayout(SHELF_NAME, parent="ShelfLayout")

    # FK / IK Switcher tool
    cmds.shelfButton(
        parent=SHELF_NAME,
        label="FK / IK Switcher",
        command=(
            "import importlib\n"
            "from tools import rig\n"
            "importlib.reload(rig)\n"
            "rig.register()\n"
        ),
        image=f"{TOOLS_ROOT}/icons/switch.png",
        sourceType="python",
        annotation="FK / IK Switcher",
    )


# register all tools HERE !
cmds.evalDeferred(create_shelf, lowestPriority=True)
