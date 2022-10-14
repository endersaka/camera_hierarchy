# SPDX-License-Identifier: GPL-2.0-or-later

from . import build_hierarchy
# from . import composition_guides_menu
# from . import prefs
# from . import ui_panels
# from . import operators
# from . import build_rigs

bl_info = {
    "name": "Add Camera Hierarchy",
    "author": "Marco Frisan",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Camera > Dolly Hierarchy",
    "description": "Adds a Camera Hierarchy",
    # "doc_url": "{BLENDER_MANUAL_URL}/addons/camera/camera_rigs.html",
    # "tracker_url": "https://github.com/waylow/add_camera_rigs/issues",
    "category": "Camera",
}


# =========================================================================
# Registration:
# =========================================================================


def register():
    build_hierarchy.register()
    # build_rigs.register()
    # operators.register()
    # ui_panels.register()
    # prefs.register()
    # composition_guides_menu.register()


def unregister():
    build_hierarchy.unregister()
    # build_rigs.unregister()
    # operators.unregister()
    # ui_panels.unregister()
    # prefs.unregister()
    # composition_guides_menu.unregister()


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
