import sys
from classes.DataBlock import DataBlock

sys.path.append(".")


class OFShader:
    def __init__(self, name=None, params=None):
        self.name = name
        self.params = params

    def fromDataBlock(self, data: DataBlock):
        self.name = data.key
        self.params = {}

        for param_block in data.inner_blocks:
            param_data = param_block.inner_blocks

            if len(param_data) == 1:
                param_data = param_data[0]
                if param_data == '*NULL*':
                    param_data = None

            if param_data is not None:
                self.params[param_block.key] = param_data
