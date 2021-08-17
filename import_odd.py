import sys
sys.path.append(".")

import os
from import_odr import *
from classes.OFodd import OFodd

def importODD(filepath):
    base_path = os.path.dirname(filepath)

    odd_obj = OFodd(filepath)

    mesh_list = []
    for odr_path in odd_obj.odr_file_pathes:
        mesh_list.append(importODR(base_path + '\\' + odr_path))
    return mesh_list

# importODD(r'C:\Users\dimaa\Desktop\u_m_o_taphillbilly.odd')