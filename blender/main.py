import os
import sys

# TODO
# ROOT_ENV
# TOOLS_ENV

TOOLS_ROOT = os.environ.get("ALCHEMY_ROOT")

if not TOOLS_ROOT:
    raise RuntimeError("DCC_TOOLS_ROOT environment variable is not set")

sys.path.append(TOOLS_ROOT)

from tools.pivot_camera import pivot_camera  # noqa: E402
from tools.rigolo import rigolo  # noqa: E402

# register all tools HERE !
pivot_camera.register()
rigolo.register()
