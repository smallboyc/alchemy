import os
import sys

# TODO
# ROOT_ENV
# TOOLS_ENV

# NOTE : a good practice with blender is to put an entry py file into the root scripts/startup.
# This enables you to run scripts everytime you run blender.
# In my point of view, I prefer to keep a separate workspace for plug-ins.
# This keeps a standard  and clean entry point for blender without any custom scripts launched in the beginning.

TOOLS_ROOT = os.environ.get("ALCHEMY_ROOT")

if not TOOLS_ROOT:
    raise RuntimeError("DCC_TOOLS_ROOT environment variable is not set")

sys.path.append(TOOLS_ROOT)

from tools.pivot_camera import pivot_camera  # noqa: E402
from tools.rigolo import rigolo  # noqa: E402

# register all tools HERE !
pivot_camera.register()
rigolo.register()
