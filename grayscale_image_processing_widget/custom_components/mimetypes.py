import mimetypes

mimetypes.init()


def guess_file_type(file_path):
    return mimetypes.guess_type(file_path)[0]


def check_file_type(file_path, file_types):
    guessed_type = guess_file_type(file_path)
    if guessed_type:
        if guessed_type.split("/")[0] in file_types:
            return True
        else:
            return False


def get_extensions_for_type(general_types):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split("/")[0] in general_types:
            subtype = mimetypes.types_map[ext].split("/")[1]
            yield ext, subtype
