import sys
import classes.OFParser as OFP

sys.path.append(".")


class OFodd:
    def __init__(self, filepath):
        block_data = OFP.parseFromFile(filepath)

        self.odr_file_pathes = [odr_path.getInnerByIndex(0) for odr_path in block_data.getAllInners()]
