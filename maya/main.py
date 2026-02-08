import os
import sys

#TODO:
# - Install the Mayapy vs code extension
# - (optional) In order to have autocomplete working I had to change "python.autoComplete.extraPaths" in the json settings for "python.analysis.extraPaths"
# add userSetup.mel with "commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;" to run python script in real time.

TOOLS_ROOT = os.environ.get("ALCHEMY_ROOT")

if not TOOLS_ROOT:
    raise RuntimeError("DCC_TOOLS_ROOT environment variable is not set")

sys.path.append(TOOLS_ROOT)

from tools.test import foo  # noqa: E402

# register all tools HERE !
foo()
