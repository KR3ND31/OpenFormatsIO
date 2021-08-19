from classes.DataBlock import DataBlock
from classes.OFParser import OFParser
from classes.OFShader import OFShader
from utils.help_utils import getFileNameByPath, getDir


class OFodr:
    def __init__(self, filepath):
        ofp = OFParser()
        block_data = ofp.parse(filepath)

        path = getDir(filepath)

        self.name = getFileNameByPath(filepath)
        self.lod_group = {}

        for lod_block in block_data.getInnerByKey("LodGroup").getAllInners():
            lod = lod_block.getInnerByIndex(0)
            if isinstance(lod, DataBlock) and lod.key.endswith(".mesh"):
                lod_path = path + '\\' + lod.key
                self.lod_group[lod_block.key] = lod_path

        self.shaders = []

        for shader_block in block_data.getInnerByKey("Shaders").inner_blocks:
            shader = OFShader()
            shader.fromDataBlock(shader_block)
            self.shaders.append(shader)

        # WIP
        # self.skeleton = block_data.getInnerByKey("Skeleton")
