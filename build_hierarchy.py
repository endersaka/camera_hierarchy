import bpy
from bpy.types import Operator
from bpy_extras import object_utils

def add_empty_with_name(context, name):
  # Create an Empty as suggested by https://blender.stackexchange.com/a/51291/71342
  # Confirmed by https://docs.blender.org/api/current/bpy.types.BlendDataObjects.html#bpy.types.BlendDataObjects.new
  # This is the lowest level to do it!
  obdata = bpy.data.objects.new(name, None)
  # And this utility is probably equivalent to use `bpy.context.scene.collection.objects.link(cameraroot_data)`
  # See https://docs.blender.org/api/current/bpy_extras.object_utils.html#bpy_extras.object_utils.object_data_add
  empty = object_utils.object_data_add(context, obdata, name=name)
  empty_id = name.lower() + '_id'
  empty[empty_id] = "%s" % name

  return empty

# Invoked by `OBJECT_OT_build_camera_hierarchy.execute()` method to generate
# the Camera objects hierarchy.
def build_camera_hierarchy(context, mode):
  """Create stuff common to all camera hierarchies."""
  # Add the camera object
  camera_name = "%s_Camera" % mode.capitalize()
  camera_obdata = bpy.data.cameras.new(camera_name)
  camera = object_utils.object_data_add(context, camera_obdata, name=camera_name)
  context.scene.camera = camera

  # Add root empty
  camera_root = add_empty_with_name(context, 'CameraRoot')

  # Add target empty
  camera_target = add_empty_with_name(context, 'CameraTarget')

  # Add Camera Location Parent empty
  camera_location_parent = add_empty_with_name(context, 'CameraLocationParent')

  # Add Camera Constraint Parent empty
  camera_constraint_parent = add_empty_with_name(context, 'CameraConstraintParent')
  
  camera_root.location = context.scene.cursor.location
  camera_target.location = camera_root.location
  camera_location_parent.location = camera_root.location + (0.0, -10.0, -10.0)
  camera.location = camera_location_parent.location
  camera_constraint_parent.location = camera_location_parent.location
  
  camera_target.parent = camera_root
  camera_target.parent_type = 'OBJECT'
  
  camera.parent = camera_constraint_parent
  camera.parent_type = 'OBJECT'

  camera_constraint_parent.parent = camera_location_parent
  camera_constraint_parent.parent_type = 'OBJECT'

  camera_location_parent.parent = camera_root
  camera_location_parent.parent_type = 'OBJECT'

  damped_track = camera_constraint_parent.constraints.new(type='DAMPED_TRACK')
  damped_track.target = camera_target
  damped_track.track_axis = 'TRACK_NEGATIVE_Z'


class OBJECT_OT_build_camera_hierarchy(Operator):
  bl_idname = "object.build_camera_hierarchy"
  bl_label = "Build Camera Hierarchy"
  bl_description = "Build a Camera Hierarchy"
  bl_options = {'REGISTER', 'UNDO'}

  mode: bpy.props.EnumProperty(items=(('DOLLY', 'Dolly', 'Dolly Hierarchy')),
                               name='mode',
                               description='Type of camera hierarchy to create.',
                               default='DOLLY')

  def execute(self, context):
    # Build the hierarchy.
    build_camera_hierarchy(context, self.mode)
    return {'FINISHED'}


# Sort of Action or Hook callback for Blender that we append to the Add Object
# > Camera menu during the registration of tthis Addon and remove during the
# unregistration.
# The result is a new Item in the menu that calls `execute()` method of the
# Operator class `OBJECT_OT_build_camera_hierarchy` when selected by the user
# interaction.
def add_camera_hierarchy_buttons(self, context):
  """Provides Camera Hierarchy entries in the Add Object > Camera menu"""
  if context.mode == 'OBJECT':
    self.layout.operator(
        OBJECT_OT_build_camera_hierarchy.bl_idname,
        text="Dolly Camera Hierarchy",
        icon="VIEW_CAMERA"
    ).mode = "DOLLY"


# Convenience list of classes to register/unregister.
classes = (
    OBJECT_OT_build_camera_hierarchy,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_camera_add.append(add_camera_hierarchy_buttons)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    bpy.types.VIEW3D_MT_camera_add.remove(add_camera_hierarchy_buttons)


if __name__ == "__main__":
    register()
