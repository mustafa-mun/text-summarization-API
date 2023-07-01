from modules.helpers.sanitize import *
import os

async def read_file(path_to_file):
    file = open(path_to_file, "r")
    sanitized_file = sanitize_text(file.read())
    return sanitized_file

def is_filename(string):
    # Check if the string is a valid file path
    if os.path.isfile(string):
        return True

    # Check if the string is a valid path
    if os.path.isdir(string):
        return True

    return False
