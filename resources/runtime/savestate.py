import os
from enum import Enum

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from sys import platform

from pathlib import Path

home = str(Path.home())

os.system("cls")

print("Platform is " + platform, ", Home directory is " + home)
if platform == "linux":
    try:
        print("Trying to create the standard Folder...")
        os.mkdir(home + "/Documents/StreamHelper")
    except FileExistsError:
        print("Folder exists!")
    standardFilePath: str = home + "/Documents/StreamHelper"
    symbol: str = "/"
    system = 0
elif platform == "win64":
    standardFilePath: str = os.getenv('LOCALAPPDATA') + "\\StreamHelper"
    symbol: str = "\\"
    system = 0
elif platform == "win32":
    standardFilePath: str = os.getenv('LOCALAPPDATA') + "\\StreamHelper"
    symbol: str = "\\"
    system = 0

# StyleSheet for the list elements
shortBorder = \
    ".QWidget {\n" \
    + "border: 1px solid black;\n" \
    + "}"

name = ""
count = 1

# States of the List Widgets
deselectItemFunctionInitiated = [False, False]
deselectListFunctionInitiated = False
lastListSelected = 0
lastItemSelected = [0, 0]

# Standard Filepath and File Names
# standardFilePath: str = os.getcwd()
# standardFileNames = {"chronoup", "chronodown", "time"} UNUSED
standardXMLNames = ['autosave', 'config', 'init']

itemorder = []


class itemType(Enum):
    NUMBER = 1
    TEXT = 2
    CERTAINTEXT = 3
    CHRONOS = 4


# Saving lists and values
saveListNames = {}
saveListValues = {}

# Masks imported and numbered
masklist = {"standard": 0}
