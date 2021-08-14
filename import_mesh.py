import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from .classes.OFMesh import OFMesh
from .classes.OFParser import OFParser
from .utils.vertex_structs import vertexStructs

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

        ofp = OFParser()
        file_dict = ofp.parse(self.filepath)

        ofMesh_obj = OFMesh(file_dict)


        scene = bpy.context.scene


        for geometry in ofMesh_obj.geometries:
            

            vertexDeclaration = vertexStructs[geometry.vertex_declaration]

            


            mesh = bpy.data.meshes.new("mesh")  # add a new mesh
            
            obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh

            mesh.from_pydata([vert[vertexDeclaration['POSITION']] for vert in geometry.vertices], [], geometry.indices)

            scene.collection.objects.link(obj)


            
            
            uvlayer = obj.data.uv_layers.new() # default naem and do_init

            obj.data.uv_layers.active = uvlayer

            if "COLOR" in vertexDeclaration:
                vcolor1 = mesh.vertex_colors.new(name="color1")

                vcolor1_array = [vert[vertexDeclaration['COLOR']] for vert in geometry.vertices]

            uv_array = [vert[vertexDeclaration['UV']] for vert in geometry.vertices]
            normal_array = [vert[vertexDeclaration['NORMAL']] for vert in geometry.vertices]

            mesh.calc_loop_triangles()

            normals = []

            for i, lt in enumerate(mesh.loop_triangles):
                for loop_index in lt.loops:
                    # set uv coordinates
                    uvlayer.data[loop_index].uv = uv_array[mesh.loops[loop_index].vertex_index]
                    # flip y axis
                    uvlayer.data[loop_index].uv[1] = 1 - uvlayer.data[loop_index].uv[1]
                    # set normals (1)
                    normals.append(normal_array[mesh.loops[loop_index].vertex_index])

                    if vcolor1:
                        vcolor1.data[loop_index].color = vcolor1_array[mesh.loops[loop_index].vertex_index]

            mesh.use_auto_smooth = True
            mesh.normals_split_custom_set(normals)

        return {'FINISHED'}
