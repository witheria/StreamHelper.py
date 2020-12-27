# This file contains the methods to edit and create folders, also some frequently used functions
import shutil

from resources.runtime.Settings.logfunctions import logWrite


def emptyDir(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except FileNotFoundError:
        logWrite("The folder could not be found!")
