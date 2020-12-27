import shutil

from resources.runtime.functions import information

"""
Not used in 0.3.0
"""


def copyFile(source, destination):
    try:
        shutil.copy(source, destination)
    except FileNotFoundError:
        information("File could not be found...")
