import shutil

from resources.runtime.functions import information


def copyFile(source, destination):
    try:
        shutil.copy(source, destination)
    except FileNotFoundError:
        information("File could not be found...")
