import sys
sys.path.append(".")

from classes.OFParser import OFParser

class OFodd:
    def __init__(self, filepath):
        ofp = OFParser()
        block_data = ofp.parse(filepath)
        
        self.odr_file_pathes = [odr_path.getInnerByIndex(0) for odr_path in block_data.getAllInners()]