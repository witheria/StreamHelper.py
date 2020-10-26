# This file contains the methods to edit and create folders, also some frequently used functions
import shutil
from os.path import join

from resources.runtime.Settings.logfunctions import logWrite

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def emptyDir(path):
    try:
        shutil.rmtree(join(path))
    except FileNotFoundError:

        logWrite("The folder could not be found!")