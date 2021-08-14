import sys
sys.path.append(".")

import os
print (os.getcwd())

from utils.help_utils import chunks
from classes.DataBlock import DataBlock
from classes.Geometry import Geometry


class OFMesh:
    def __init__(self, block_data: DataBlock):
        self.locked = bool(block_data.getInnerByKey('Locked').getInnerByIndex(0))
        self.skinned = bool(block_data.getInnerByKey('Skinned').getInnerByIndex(0))
        self.bone_count = int(block_data.getInnerByKey('BoneCount').getInnerByIndex(0))
        self.mask = int(block_data.getInnerByKey('Mask').getInnerByIndex(0))
        # self.bounds

        self.geometries = []

        for geometry in block_data.getInnerByKey('Geometries').getInnersByKey('Geometry'):
            vertices = []
            indices = []

            shader_index = geometry.getInnerByKey('ShaderIndex').getInnerByIndex(0)
            flags = geometry.getInnerByKey('Flags').getInnerByIndex(0)
            vertex_declaration = geometry.getInnerByKey('VertexDeclaration').getInnerByIndex(0)

            vertices_array = geometry.getInnerByKey('Vertices').getAllInners()
            for vert_block in vertices_array:
                vertices_data = vert_block.getInnerByIndex(0).split(' / ')
                mapped_vertices = list(map(lambda x: [float(item) for item in x.split(' ')], vertices_data))

                vertices.append(mapped_vertices)

            incides_array = geometry.getInnerByKey('Indices').getAllInners()
            for indice_block in incides_array:
                indices_data = indice_block.getInnerByIndex(0).split(' ')
                indices_data = [int(item) for item in indices_data]

                indices.extend(chunks(indices_data, 3))

            geometry_obj = Geometry(shader_index, flags, vertex_declaration, indices, vertices)

            self.geometries.append(geometry_obj)
