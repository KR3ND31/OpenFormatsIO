import sys
sys.path.append(".")

from classes.OFParser import OFParser
from utils.help_utils import getFileNameByPath

class OFodr:
    def __init__(self, filepath):
        ofp = OFParser()
        block_data = ofp.parse(filepath)
        
        self.name = getFileNameByPath(filepath)
        self.lod_group = block_data.getInnerByKey("LodGroup")
        self.shaders = block_data.getInnerByKey("Shaders")
        self.skel = block_data.getInnerByKey("Skeleton")