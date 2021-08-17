import bpy
from .import_mesh import *

class GtaIOPanel(bpy.types.Panel):
    """Panel containing import/export options in the Scene tab"""
    bl_label = "OpenFormat I/O"
    bl_idname = "SCENE_PT_OF_IO"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
      
        row = layout.row()
        row.operator(ImportGta5Mesh.bl_idname, text="Import GTA5 Ped Mesh (.mesh)")
        row.operator(SelectDirExample.bl_idname, text="Import GTA5 Ped Meshes (.mesh)")
        pass
