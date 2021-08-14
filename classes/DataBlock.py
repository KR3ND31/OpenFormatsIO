class DataBlock:
    def __init__(self, block_key=None, inner_blocks=None):
        if inner_blocks is None:
            inner_blocks = []
        if not isinstance(inner_blocks, list):
            inner_blocks = [inner_blocks]

        self.key = block_key
        self.inner_blocks = inner_blocks
        pass

    def addInnerDataBlock(self, data_block):
        self.inner_blocks.append(data_block)

    def getInnerByKey(self, block_key):
        for block in self.inner_blocks:
            if isinstance(block, DataBlock):
                if block.key == block_key:
                    return block
        return None

    def getInnersByKey(self, block_key):
        ret_blocks = []
        for block in self.inner_blocks:
            if isinstance(block, DataBlock):
                if block.key == block_key:
                    ret_blocks.append(block)
        return ret_blocks if len(ret_blocks) > 0 else None

    def getInnerByIndex(self, index):
        return self.inner_blocks[index] if index < len(self.inner_blocks) else None

    def getAllInners(self):
        return self.inner_blocks
