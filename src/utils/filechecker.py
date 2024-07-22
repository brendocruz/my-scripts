import os


def file_ouptut_checker(filename: str, overwrite: bool=False):
    """Check if a file already exists and raise `FileExistsError` 
    if true and overwrite is not allowed. Always raise `FileExistsError`
    is the file already exists as a directory.

    Arguments:
    filename  -- the filename.
    overwrite -- if the new file can overwrite the old one.
    """
    if os.path.isfile(filename) and not overwrite:
        message = f'File `{filename}` already exists.'
        raise FileExistsError(message)

    if os.path.isdir(filename):
        message = f'File `{filename} already exists as a directory.`'
        raise FileExistsError(message)
