import bpy


# Object
class PivotCamera:
    def __init__(
        self,
        name="PivotCamera",
        camera_location=(4.03, -0.69, 1.69),
        camera_rotation=(1.16588, 0.0, 1.08909),
        pivot_location=(0, 0, 0),
    ):
        self.name = name
        self.camera = None
        self.pivot = None

        self._create_pivot(pivot_location)
        self._create_camera(camera_location, camera_rotation)
        self._parent_camera_to_pivot()

    def _create_pivot(self, location):
        pivot = bpy.data.objects.new(f"{self.name}_Pivot", None)
        bpy.context.scene.collection.objects.link(pivot)

        pivot.empty_display_type = "ARROWS"
        pivot.empty_display_size = 1.0
        pivot.location = location

        self.pivot = pivot

    def _create_camera(self, location, rotation):
        cam_data = bpy.data.cameras.new(f"{self.name}_CameraData")
        cam = bpy.data.objects.new(f"{self.name}_Camera", cam_data)
        bpy.context.scene.collection.objects.link(cam)

        cam.location = location
        cam.rotation_euler = rotation

        self.camera = cam

    def _parent_camera_to_pivot(self):
        self.camera.parent = self.pivot

    def delete(self):
        bpy.data.objects.remove(self.camera, do_unlink=True)
        bpy.data.objects.remove(self.pivot, do_unlink=True)


# Operator
class PivotCameraOperator(bpy.types.Operator):
    bl_idname = "object.pivot_camera"
    bl_label = "Pivot Camera Operator"
    bl_description = "Camera with Pivot rotation"

    def execute(self, context):
        PivotCamera()
        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(
        PivotCameraOperator.bl_idname, text="Camera Pivot", icon="CAMERA_DATA"
    )


# Main function

def register():
    bpy.utils.register_class(PivotCameraOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)
