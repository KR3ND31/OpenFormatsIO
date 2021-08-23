from classes.DataBlock import DataBlock
from classes.OFGeometry import OFGeometry
import classes.OFParser as OFP
from utils.help_utils import strToBool


class OFMesh:
    def __init__(self, filepath):
        block_data = OFP.parseFromFile(filepath)

        self.locked = strToBool(block_data.getInnerByKey('Locked').getInnerByIndex(0))
        self.skinned = strToBool(block_data.getInnerByKey('Skinned').getInnerByIndex(0))
        self.bone_count = int(block_data.getInnerByKey('BoneCount').getInnerByIndex(0))
        self.mask = int(block_data.getInnerByKey('Mask').getInnerByIndex(0))

        # wip
        self.bounds = block_data.getInnerByKey('Bounds')
        
        self.geometries = []

        for geometry in block_data.getInnerByKey('Geometries').getInnersByKey('Geometry'):
            geometry_obj = OFGeometry(geometry)
            self.geometries.append(geometry_obj)

    def toDataBlock(self):
        locked_block = DataBlock('Locked', self.locked)
        skinned_block = DataBlock('Skinned', self.skinned)
        bone_count_block = DataBlock('BoneCount', self.bone_count)
        mask_block = DataBlock('Mask', self.mask)

        # wip
        bounds_block = self.bounds

        geometries_block = DataBlock('Geometries', [geometry.toDataBlock() for geometry in self.geometries])

        root_block = DataBlock(inner_blocks=[locked_block, skinned_block, bone_count_block, mask_block, geometries_block, bounds_block])
        return root_block

