import sys

# sys.path.append(".")

import os
from utils.help_utils import clearStr, is_number
from classes.DataBlock import DataBlock


class OFParser:
    def parse(self, file_path):
        if os.path.isfile(file_path):
            f = open(file_path)
            content = f.readlines()

            content = content[2:-1]  # Delete version information

            block = DataBlock(inner_blocks=self.__blockParse(content))

            return block
        return False

    def __blockParse(self,
                     block_data):  # Function that parses OpenFormats files(.odd/.odr/.bound/.otx/.skel/.mesh) and converts to dict type

        inner_blocks_obj = []
        inner_block_data = []
        block_start_index = 0
        block_tab_index = 0

        for index in range(len(block_data)):

            if '}' in block_data[index]:
                block_tab_index -= 1

            if block_tab_index > 0:
                inner_block_data.append(block_data[index])

            if '{' in block_data[index]:
                if block_tab_index == 0:
                    block_start_index = index - 1
                block_tab_index += 1

            if block_tab_index == 0:
                if '{' not in block_data[index] and '}' not in block_data[index]:
                    if index == len(block_data) - 1 or '{' not in block_data[index + 1]:
                        clear_line = clearStr(block_data[index])

                        line_data = clear_line.split(' ')

                        if not is_number(line_data[0]) and len(line_data) > 1:
                            inner_blocks_obj.append(DataBlock(line_data[0], line_data[1:]))
                        else:
                            inner_blocks_obj.append(DataBlock(inner_blocks=clear_line))

                if len(inner_block_data) and index != 0:
                    block_name_line = block_data[block_start_index]
                    block_name = clearStr(
                        block_name_line.split(' ')[0])  # Сlearing unnecessary information (ex. Indices 1512 -> Incides)

                    inner_blocks_obj.append(
                        DataBlock(block_name, self.__blockParse(inner_block_data)))  # Recursive call of the indoor unit

                    inner_block_data = []
                continue

        return inner_blocks_obj
