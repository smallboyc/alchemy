import maya.cmds as cmds


def foo():
    cmds.polyCube(sx=5, sy=5, sz=5)
    w = cmds.polyCube("polyCube1", q=True, w=True)


# dev mod (only executed if you run this script in a current maya project)
if __name__ == "__main__":
    print("Hello dev mode")
