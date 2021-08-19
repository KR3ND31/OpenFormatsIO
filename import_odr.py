from classes.OFodr import OFodr
from import_mesh import importMesh


def importODR(filepath, **kwargs):
    odr_obj = OFodr(filepath)

    # get LOD
    LODs = []
    match = False
    for lod_key in odr_obj.lod_group:
        lod_val = odr_obj.lod_group[lod_key]
        LODs.append(lod_val)

        if kwargs.get("LOD") == lod_key:
            match = True
            mesh_path = lod_val

    # if no match take highest LOD
    if not match:
        print('LOD not found, take highest available')
        mesh_path = LODs[0]

    blender_obj = importMesh(mesh_path)

    return blender_obj
