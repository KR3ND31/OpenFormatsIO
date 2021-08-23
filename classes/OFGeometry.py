from classes.DataBlock import DataBlock
from utils.help_utils import chunks, merge


class OFGeometry:
    def __init__(self, geometry_block):
        vertices = []
        indices = []

        shader_index = int(geometry_block.getInnerByKey('ShaderIndex').getInnerByIndex(0))
        flags = geometry_block.getInnerByKey('Flags').getInnerByIndex(0)
        vertex_declaration = geometry_block.getInnerByKey('VertexDeclaration').getInnerByIndex(0)

        vertices_array = geometry_block.getInnerByKey('Vertices').getAllInners()
        for vert_block in vertices_array:
            vertices_data = vert_block.getInnerByIndex(0).split(' / ')
            mapped_vertices = list(map(lambda x: [float(item) for item in x.split(' ')], vertices_data))

            vertices.append(mapped_vertices)

        incides_array = geometry_block.getInnerByKey('Indices').getAllInners()
        for indice_block in incides_array:
            indices_data = indice_block.getInnerByIndex(0).split(' ')
            indices_data = [int(item) for item in indices_data]

            indices.extend(chunks(indices_data, 3))

        self.shader_index = shader_index
        self.flags = flags
        self.vertex_declaration = vertex_declaration
        self.indices = indices
        self.vertices = vertices

    def toDataBlock(self):
        shader_block = DataBlock('ShaderIndex', self.shader_index)
        flags_block = DataBlock('Flags', self.flags)
        vertex_declaration_block = DataBlock('VertexDeclaration', self.vertex_declaration)

        vertices_count = len(self.vertices)
        vertices_DataBlock_list = []
        for vertex_data in self.vertices:
            vertices_DataBlock_list.append(DataBlock(
                inner_blocks=[' / '.join(' '.join([str(item) for item in vertex]) for vertex in vertex_data)]))
        vertices_block = DataBlock('Vertices ' + str(vertices_count), vertices_DataBlock_list)

        indices_count = len(self.indices) * 3
        indices_DataBlock_list = []
        for indice_data in chunks(self.indices, 5):
            merged_data = merge(*indice_data)

            indices_DataBlock_list.append(DataBlock(
                inner_blocks=' '.join([str(item) for item in merged_data])))
        indices_block = DataBlock('Indices ' + str(indices_count), indices_DataBlock_list)

        root_block = DataBlock('Geometry',
                               [shader_block, flags_block, vertex_declaration_block, indices_block, vertices_block])
        return root_block
