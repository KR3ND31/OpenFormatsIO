import sys

# sys.path.append(".")

import os
from utils.help_utils import clearStr, is_number
from classes.DataBlock import DataBlock

VERSION = 'Version 165 32'


def parseFromFile(file_path):
    if os.path.isfile(file_path):
        f = open(file_path)
        content = f.readlines()
        f.close()
        content = content[2:-1]  # Delete version information

        block = DataBlock(inner_blocks=__blockParse(content))

        return block
    return False


def __blockParse(block_data):
    """Function that parses OpenFormats files(.odd/.odr/.bound/.otx/.skel/.mesh) and converts to DataBlock objects"""

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

                    # if not is_number(line_data[0]) and len(line_data) > 1:
                    #     inner_blocks_obj.append(DataBlock(line_data[0], line_data[1:]))
                    # else:
                    #     inner_blocks_obj.append(DataBlock(inner_blocks=clear_line))
                    # OR
                    # inner_blocks_obj.append(DataBlock(inner_blocks=clear_line))
                    if not is_number(line_data[0]) and len(line_data) == 2:
                        inner_blocks_obj.append(DataBlock(line_data[0], line_data[1]))
                    else:
                        inner_blocks_obj.append(DataBlock(inner_blocks=clear_line))


            if len(inner_block_data) and index != 0:
                block_name_line = block_data[block_start_index]
                block_name = clearStr(
                    block_name_line.split(' ')[0])  # Сlearing unnecessary information (ex. Indices 1512 -> Incides)

                inner_blocks_obj.append(
                    DataBlock(block_name, __blockParse(inner_block_data)))  # Recursive call of the indoor unit

                inner_block_data = []
            continue

    return inner_blocks_obj


def saveToFile(file_path, block_data: DataBlock):
    data_str = VERSION + '\n{\n' + __blockToStr(block_data, tab_level=1) + '}'
    f = open(file_path, "w")
    f.write(data_str)
    f.close()


def __blockToStr(block_data: DataBlock, tab_level=0):
    """Function that convert DataBlock objects to OpenFormats files(.odd/.odr/.bound/.otx/.skel/.mesh)"""

    ret_str = ''

    if not isinstance(block_data, DataBlock):
        ret_str += '\t' * tab_level + str(block_data) + '\n'
        return ret_str

    if block_data.key is None:
        for block in block_data.inner_blocks:
            ret_str += __blockToStr(block, tab_level)
    else:
        ret_str += '\t' * tab_level + block_data.key

        if len(block_data.inner_blocks) == 1 and not isinstance(block_data.getInnerByIndex(0), DataBlock):
            ret_str += ' ' + str(block_data.getInnerByIndex(0)) + '\n'
        else:
            ret_str += '\n' + '\t' * tab_level + '{\n'
            for block in block_data.inner_blocks:
                ret_str += __blockToStr(block, tab_level + 1)
            ret_str += '\t' * tab_level + '}\n'
    return ret_str
