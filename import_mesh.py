import numpy as np
import sys
sys.path.append(".")

import bpy

from classes.OFMesh import OFMesh
from utils.vertex_structs import vertexStructs
from utils.help_utils import getFileNameByPath


def importMesh(filepath):
    blender_obj = []

    obj_name = getFileNameByPath(filepath)

    ofMesh_obj = OFMesh(filepath)

    for num, geometry in enumerate(ofMesh_obj.geometries):
        vertexDeclaration = vertexStructs[geometry.vertex_declaration]

        name = obj_name + '_' + str(num)
        verts = [vert[vertexDeclaration['POSITION']] for vert in geometry.vertices]
        faces = geometry.indices
        shaderIndex = geometry.shader_index

        mesh = bpy.data.meshes.new("mesh")  # add a new mesh
        mesh.from_pydata(verts, [], faces)

        obj = bpy.data.objects.new(name, mesh)  # add a new object using the mesh

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


        blender_obj.append(obj)

    return blender_obj
