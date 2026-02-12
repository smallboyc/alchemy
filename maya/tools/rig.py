import maya.cmds as cmds
from PySide6 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
from enum import Enum

# /!\ shiboken is used to transform C++ Maya Qt objects to python objects


def maya_main_window():
    """Return Maya's main window as a PySide QWidget.

    Maya's UI is implemented in C++ (Qt).
    "ptr" is a pointer to the C++ QMainWindow.
    "wrapInstance" converts "ptr" into a Python Qt object (QWidget)
    """
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class Mode(float, Enum):
    IK = 0
    FK = 1


def switch_mode(ik_fk_switch_name: str) -> Mode | None:
    if not cmds.objExists(ik_fk_switch_name):
        cmds.warning(f"Object not found: {ik_fk_switch_name}")
        return None

    switch_attr = f"{ik_fk_switch_name}.FK_IK_Switch"
    if not cmds.objExists(switch_attr):
        cmds.warning(f"Attribute not found: {switch_attr}")
        return None

    current = cmds.getAttr(switch_attr)
    if current is None:
        cmds.warning("No FK/IK switch value found.")
        return None

    current_mode = Mode.IK if float(current) == float(Mode.IK.value) else Mode.FK
    new_mode = Mode.FK if current_mode == Mode.IK else Mode.IK

    cmds.setAttr(switch_attr, float(new_mode.value))
    return new_mode


def toggle_visibility(mode: Mode) -> None:
    excludes = ["Switch"]

    hide_mode = "IK" if mode == Mode.FK else "FK"
    show_mode = "FK" if mode == Mode.FK else "IK"

    for item in cmds.ls(type="transform") or []:
        if not cmds.attributeQuery("visibility", node=item, exists=True):
            continue

        if show_mode in item:
            cmds.setAttr(f"{item}.visibility", 1)
        elif hide_mode in item and not any(ex in item for ex in excludes):
            cmds.setAttr(f"{item}.visibility", 0)


class FKIKWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FK/IK Toggle")

        # instantiate widgets
        self.search = QtWidgets.QLineEdit()
        self.pick_btn = QtWidgets.QPushButton("Use Selection")
        self.toggle_btn = QtWidgets.QPushButton("Toggle FK/IK")
        self.status_lbl = QtWidgets.QLabel("Ready.")

        # search + use seleted object (switch)
        row = QtWidgets.QHBoxLayout()
        self.search.setPlaceholderText("Switch node name (ex: FK_IK_Switch_Arm_L)")
        row.addWidget(self.search)
        row.addWidget(self.pick_btn)

        # create final layout and add it to the window (with self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.status_lbl)

        # callbacks
        self.pick_btn.clicked.connect(self.on_pick_selection)
        self.toggle_btn.clicked.connect(self.on_toggle)

        self.resize(420, 120)

    def on_pick_selection(self):
        sel = cmds.ls(sl=True) or []
        if not sel:
            self.status_lbl.setText("No selection.")
            return
        self.search.setText(sel[0])
        self.status_lbl.setText(f"Using: {sel[0]}")

    def on_toggle(self):
        node = self.search.text().strip()
        if not node:
            self.status_lbl.setText("Enter a switch node name.")
            return

        new_mode = switch_mode(node)
        if new_mode is None:
            self.status_lbl.setText("Toggle failed (check node/attr).")
            return

        toggle_visibility(new_mode)
        self.status_lbl.setText(f"Switched to: {new_mode.name}")


def register() -> None:
    window = FKIKWindow(parent=maya_main_window())
    window.show()


# dev mod
if __name__ == "__main__":
    register()
