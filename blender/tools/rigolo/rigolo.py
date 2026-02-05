import bpy
from enum import Enum

# TODO : Disable plugin if the user is not in POSE mode.

FK_LOCATION = 0.0
IK_LOCATION = 2.0


class BoneType(Enum):
    SWITCH = "SWITCH_CT"
    FK = "FK_CT"
    IK = "IK_CT"


def get_bones_data(bone_type: BoneType) -> list[bpy.types.PoseBone]:
    """Get access to specific bone(s) in Arm_Rig"""
    data = []

    for obj in bpy.data.objects:
        if obj.type != "ARMATURE" or obj.mode != "POSE":
            continue
        if obj.name != "Arm_Rig":
            continue

        # # Switch bone
        if bone_type == BoneType.SWITCH:
            try:
                return [obj.pose.bones[bone_type.value]]
            except KeyError:
                return []

        # FK / IK bones
        for bone in obj.pose.bones:
            if bone_type.value in bone.name:
                data.append(bone)

    return data


def switch_mode():
    """Set FK or IK mode."""
    switch_bone = get_bones_data(BoneType.SWITCH)
    if switch_bone:
        location = (
            FK_LOCATION if switch_bone[0].location.z == IK_LOCATION else IK_LOCATION
        )
        switch_bone[0].location.z = location


def get_current_mode_label() -> str:
    """Get a simple string for the FK/IK mode"""
    switch_bone = get_bones_data(BoneType.SWITCH)
    if not switch_bone:
        return "Unknown"
    return "FK" if switch_bone[0].location.z == FK_LOCATION else "IK"


class RIGOLO_OT_toggle_fk_ik(bpy.types.Operator):
    """
    Custom Operator:
    - Toggle FK / IK
    - needs to set a switch (driver) before
    """

    bl_idname = "rigolo.toggle_fk_ik"
    bl_label = "Toggle FK / IK"

    def execute(self, context):
        switch_mode()
        return {"FINISHED"}


class VIEW3D_PT_Rigolo(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rigolo"
    bl_label = "Rigolo"

    def draw(self, context):
        self.layout.label(text=f"Current Mode : {get_current_mode_label()}")
        self.layout.operator("rigolo.toggle_fk_ik", text="Toggle FK / IK")


class RIGOLO_OT_match_fk_ik_transform(bpy.types.Operator):
    bl_idname = "rigolo.match_fk_ik_transform"
    bl_label = "Match FK / IK transform"

    def execute(self, context):
        return {"FINISHED"}


# Register
def register():
    bpy.utils.register_class(RIGOLO_OT_toggle_fk_ik)
    bpy.utils.register_class(VIEW3D_PT_Rigolo)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_Rigolo)
    bpy.utils.unregister_class(RIGOLO_OT_toggle_fk_ik)
