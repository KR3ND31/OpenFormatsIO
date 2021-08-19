import sys
# sys.path.append(".")

import os
from import_odr import importODR
from classes.OFodd import OFodd



def importODD(filepath, **kwargs):
    base_path = os.path.dirname(filepath)

    odd_obj = OFodd(filepath)

    mesh_list = []
    for odr_path in odd_obj.odr_file_pathes:
        mesh_list.append(importODR(base_path + '\\' + odr_path, **kwargs))

    return mesh_list
