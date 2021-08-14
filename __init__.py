import bpy

bl_info = {
    "name": "OpenFormat I/O (.odr)",
    "author": "KR3ND31",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}

from . import auto_load

auto_load.init()


def register():
    auto_load.register()


def unregister():
    auto_load.unregister()
