import os
from enum import Enum

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

os.system("cls")

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
standardFilePath: str = os.getenv('LOCALAPPDATA') + "\\StreamHelper"
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
