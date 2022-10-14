import bpy
from bpy.types import Operator
from bpy_extras import object_utils
from mathutils import Vector

def add_empty_with_name(context, name):
  # An Empty can be created like suggested by https://blender.stackexchange.com/a/51291/71342
  # Confirmed by https://docs.blender.org/api/current/bpy.types.BlendDataObjects.html#bpy.types.BlendDataObjects.new
  # This is the lowest level to do it!
  # Thought there is a easyer way to do it...
  # And this utility is probably equivalent to use the previous one in combination with
  # `bpy.context.scene.collection.objects.link(cameraroot_data)`
  # See https://docs.blender.org/api/current/bpy_extras.object_utils.html#bpy_extras.object_utils.object_data_add
  empty = object_utils.object_data_add(context, None, name=name)
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
  
  # Set required locations
  camera_root.location = context.scene.cursor.location
  camera_target.location = (0.0, 0.0, 0.0)
  camera_location_parent.location = (0.0, -10.0, 10.0)
  
  # Setup hierarchy
  camera_target.parent = camera_root
  camera_target.parent_type = 'OBJECT'
  
  camera.parent = camera_constraint_parent
  camera.parent_type = 'OBJECT'

  camera_constraint_parent.parent = camera_location_parent
  camera_constraint_parent.parent_type = 'OBJECT'

  camera_location_parent.parent = camera_root
  camera_location_parent.parent_type = 'OBJECT'

  damped_track = camera_constraint_parent.constraints.new(type='TRACK_TO')
  damped_track.target = camera_target
  damped_track.track_axis = 'TRACK_NEGATIVE_Z'
  damped_track.up_axis = 'UP_Y'


class OBJECT_OT_build_camera_hierarchy(Operator):
  bl_idname = "object.build_camera_hierarchy"
  bl_label = "Build Camera Hierarchy"
  bl_description = "Build a Camera Hierarchy"
  bl_options = {'REGISTER', 'UNDO'}
  
  mode: bpy.props.EnumProperty(
    items=(
      ('DOLLY', 'Dolly', 'Dolly rig'),
      ('CRANE', 'Crane', 'Crane rig',),
      ('2D', '2D', '2D rig')
    ),
    name="mode",
    description="Type of camera to create",
    default="DOLLY"
  )

  def execute(self, context):
    # Build the hierarchy.
    build_camera_hierarchy(context, self.mode)
    return {'FINISHED'}


# Draw function that populates the `Add Object > Camera` menu with our custom
# menu items.
#
# It is appended to the existing draw functions during the registration phase
# of this Addon and removed during the unregistration phase.
#
# The result so far is a new Item in the menu that calls `execute()` method of
# the Operator class `OBJECT_OT_build_camera_hierarchy` when selected by user
# interaction.
#
# `self` and `context` are set by the caller that is the object to wich this
# function is appended as can be easyly understood reading
# https://docs.blender.org/api/current/bpy.types.Menu.html#extending-menus
def draw_camera_hierarchy_menu_items(self, context):
  """Provides Camera Hierarchy entries in the Add Object > Camera menu"""
  if context.mode == 'OBJECT':
    self.layout.operator(
        OBJECT_OT_build_camera_hierarchy.bl_idname,
        text="Dolly Camera Hierarchy",
        icon="VIEW_CAMERA"
    ).mode = "DOLLY"


def append_draw_function():
    bpy.types.VIEW3D_MT_camera_add.append(draw_camera_hierarchy_menu_items)


def remove_draw_function():
    bpy.types.VIEW3D_MT_camera_add.remove(draw_camera_hierarchy_menu_items)

# Convenience list of classes to register/unregister.
classes = (
    OBJECT_OT_build_camera_hierarchy,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    append_draw_function()


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    remove_draw_function()

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
