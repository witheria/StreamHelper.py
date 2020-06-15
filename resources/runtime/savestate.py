import random
from enum import Enum
from importlib import resources
from pathlib import Path

import pickle
import os
from typing import List, Any

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from PyQt5.QtCore import QModelIndex

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
standardFileNames = {"chronoup", "chronodown", "time"}
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
