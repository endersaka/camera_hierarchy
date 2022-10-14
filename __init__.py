# SPDX-License-Identifier: GPL-2.0-or-later

from . import build_hierarchy

bl_info = {
    "name": "Add Camera Hierarchy",
    "author": "Marco Frisan",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Camera > Dolly Hierarchy",
    "description": "Adds a Camera Hierarchy",
    # "doc_url": "",
    # "tracker_url": "",
    "category": "Camera",
}


# =========================================================================
# Registration:
# =========================================================================


def register():
    build_hierarchy.register()


def unregister():
    build_hierarchy.unregister()


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
