import numpy as np
import os

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import (
        StringProperty,
        CollectionProperty,
        )
from bpy.types import (
        Operator,
        OperatorFileListElement,
        )

from .classes.OFMesh import OFMesh
from .classes.OFParser import OFParser
from .utils.vertex_structs import vertexStructs
from .utils.help_utils import findFilesByExt, getFileNameByPath

from mathutils import (Vector)

class ImportGta5Mesh(Operator, ImportHelper):
    """Imports a mesh object with UVs and weights (but no skeleton) as declared in the .mesh file"""
    bl_idname = "io_gta5ped.import_mesh"
    bl_label = "Import GTA5 Ped Mesh (.mesh)"

    # ImportHelper mixin class uses this
    filename_ext = ".mesh"

    filter_glob: StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        filename = getFileNameByPath(self.filepath)
        mesh_obj = OFMesh(self.filepath)

        addOFMeshToScene(filename, mesh_obj)
        return {'FINISHED'}

class ImportGta5Meshes(Operator, ImportHelper):
    """Imports a mesh objects with UVs and weights (but no skeleton) as declared in the .mesh file"""
    bl_idname = "io_gta5ped.import_meshes"
    bl_label = "Import GTA5 Ped Meshes (.mesh)"

    files:CollectionProperty(
            name="File Path",
            type=OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'},
            )
    directory:StringProperty(
            subtype='DIR_PATH',
            )

    filename_ext = ""

    def execute(self, context):
        import os
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            print(filepath)
        return {'FINISHED'}


class SelectDirExample(bpy.types.Operator):

    """Create render for all chracters"""
    bl_idname = "example.select_dir"
    bl_label = "Select Dir"
    bl_options = {'REGISTER'}

    # Define this to tell 'fileselect_add' that we want a directoy
    directory:bpy.props.StringProperty(
        name="Outdir Path",
        description="Where I will save my stuff"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
        )

    def execute(self, context):
        mesh_files = findFilesByExt(self.directory, 'mesh')

        for mesh_file_path in mesh_files:
            filename = getFileNameByPath(mesh_file_path)

            mesh_obj = OFMesh(mesh_file_path)
            addOFMeshToScene(filename, mesh_obj)

        return {'FINISHED'}

    def invoke(self, context, event):
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}

def addOFMeshToScene(obj_name: str, ofMesh_obj: OFMesh):

    scene = bpy.context.scene


    for num, geometry in enumerate(ofMesh_obj.geometries):
        vertexDeclaration = vertexStructs[geometry.vertex_declaration]

        name = obj_name + str(num)
        verts = [vert[vertexDeclaration['POSITION']] for vert in geometry.vertices]
        faces = geometry.indices
        shaderIndex = geometry.shader_index
        
        mesh = bpy.data.meshes.new("mesh")  # add a new mesh
        mesh.from_pydata(verts, [], faces)
        
        obj = bpy.data.objects.new(name, mesh)  # add a new object using the mesh
        
        scene.collection.objects.link(obj)

        
        uvlayer = obj.data.uv_layers.new() # default name and do_init

        obj.data.uv_layers.active = uvlayer

        if "COLOR" in vertexDeclaration:
            vcolor1 = mesh.vertex_colors.new(name="color1")
            vcolor1_array = [vert[vertexDeclaration['COLOR']] for vert in geometry.vertices]

        if "UV" in vertexDeclaration:
            uv_array = [vert[vertexDeclaration['UV']] for vert in geometry.vertices]

        if "NORMAL" in vertexDeclaration:
            normal_array = [vert[vertexDeclaration['NORMAL']] for vert in geometry.vertices]

        mesh.calc_loop_triangles()

        normals = []

        for i, lt in enumerate(mesh.loop_triangles):
            for loop_index in lt.loops:

                if "UV" in vertexDeclaration:
                    # set uv coordinates
                    uvlayer.data[loop_index].uv = uv_array[mesh.loops[loop_index].vertex_index]
                    # flip y axis
                    uvlayer.data[loop_index].uv[1] = 1 - uvlayer.data[loop_index].uv[1]
                if "NORMAL" in vertexDeclaration:   
                    # set normals (1)
                    normals.append(normal_array[mesh.loops[loop_index].vertex_index])
                if vcolor1:
                    vcolor1.data[loop_index].color = np.array(vcolor1_array[mesh.loops[loop_index].vertex_index])/255

        mesh.use_auto_smooth = True

        if "NORMAL" in vertexDeclaration:
            mesh.normals_split_custom_set(normals)
