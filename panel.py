import bpy
from .import_odd import *
from .import_mesh import *

from bpy_extras.io_utils import ImportHelper
from bpy.props import (
        StringProperty,
        CollectionProperty,
        BoolProperty,
        EnumProperty
        )
from bpy.types import (
        Operator,
        OperatorFileListElement,
        )

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
        # row.operator(SelectDirExample.bl_idname, text="Import GTA5 Ped Meshes (.mesh)")
        row.operator(ImportGta5ODD.bl_idname, text="Import GTA5 ODD File (.odd)")
        pass


class ImportGta5Mesh(Operator, ImportHelper):
    """Imports a mesh objects with UVs and weights (but no skeleton) as declared in the .mesh file"""
    bl_idname = "io_gta5ped.import_mesh"
    bl_label = "Import OF .mesh File"

    files:CollectionProperty(
            name="Mesh Files",
            type=OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
            )
    directory:StringProperty(
            subtype='DIR_PATH',
            )

    # ImportHelper mixin class uses this
    filename_ext = ".mesh"

    filter_glob: StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        import os
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            
            blender_obj = importMesh(filepath)

            scene = bpy.context.scene

            for blender_mesh in blender_obj:
                scene.collection.objects.link(blender_mesh)

        return {'FINISHED'}


class ImportGta5ODD(Operator, ImportHelper):
    """Import GTA5 ODD File include (/Shaders, Skeleton) and Mesh (.odd)"""
    bl_idname = "io_gta5ped.import_odd"
    bl_label = "Import .odd File"
    bl_options = {'REGISTER'}

    files:CollectionProperty(
            name="ODD Files",
            type=OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
            )
    directory:StringProperty(
            subtype='DIR_PATH',
            )

    #  Custom settings
    LOD: EnumProperty(
        name="LOD",
        description="If the LOD does not exist, the largest will be loaded",
        items=[
            ("High", "High", "High", 1),
            ("Med", "Med", "Med", 2),
            ("Low", "Low", "Low", 3),
            ("Vlow", "Vlow", "Vlow", 4),
        ],
        default="High",
        options=set()
    )

    # create_materials: EnumProperty(
    #     name="Create Materials",
    #     description="Auto will use existing material or create new one.",
    #     items=[
    #         ("no", "No", "no materials", 1),
    #         ("create", "Create", "force material creation", 2),
    #         ("auto", "Auto", "materials can be reused", 3),
    #     ],
    #     default="auto",
    #     options=set()
    # )

    # ImportHelper mixin class uses this
    filename_ext = ".odd"

    filter_glob: StringProperty(
        default="*.odd",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        import os
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            
            blender_objs = importODD(filepath, LOD=self.LOD)

            scene = bpy.context.scene

            for blender_obj in blender_objs:
                for blender_mesh in blender_obj:
                    scene.collection.objects.link(blender_mesh)

        return {'FINISHED'}
