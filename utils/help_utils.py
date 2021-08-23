def clearStr(string):
    return string.replace('\n', '').replace('\t', '')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def merge(*iters):
    for it in iters:
        yield from it


def findFilesByExt(path, ext):
    import os
    ret_files_path = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("." + ext):
                path_file = os.path.join(root, file)
                ret_files_path.append(path_file)
    return ret_files_path


def getFileNameByPath(filepath):
    import os
    filename = os.path.basename(filepath)
    index = filename.index('.')
    return filename[:index]


def getDir(filepath):
    import os
    return os.path.dirname(filepath)


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def strToBool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))