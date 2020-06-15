import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication

from resources.runtime import savestate
from resources.runtime.functions import information, activateUi, updateSelection, createStandardFiles, createTextFiles
from resources.runtime.interactions import addListElement, setFilePath, autTextListElement, getTextOfItem, createListFiles

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from resources.runtime.savestate import standardFilePath

import webbrowser


class uiControlTest(QMainWindow):
    """uncomment this to output a logfile"""

    # old_stdout = sys.stdout
    # log_file = open("message.log", "w")
    # sys.stdout = log_file

    def __init__(self):
        super(uiControlTest, self).__init__()

        # Basic loading and startup operations
        self.ui = uic.loadUi('main.ui')
        window = self.ui
        window.setWindowIcon(QIcon("images\\icon.png"))
        information("The Program is in developement! \n"
                    "Currently, only the textfiles are working, numbers and the other stuff are WIP. Masks aren't "
                    "importable yet")
        self.ui.show()

        # Check if the folder exists
        try:
            print("Trying to create the standard Folder...")
            os.mkdir(os.getenv('LOCALAPPDATA') + "\\StreamHelper")
        except FileExistsError:
            print("Folder exists!")

        # Lets create all the standard files (xml and txt) or at least check if they exist
        createStandardFiles(standardFilePath, 0)

        # Parse the paths from the xml files so we know where to check for the files
        tree = ET.parse(standardFilePath + "\\config.xml")
        root = tree.getroot()
        dictStandard = root[0][1].attrib
        dictCustom = root[0][0].attrib

        oldFilePath = dictStandard["path"]
        newFilePath = dictCustom["path"]

        # Set the read filepath so we got it internally to work with
        savestate.standardFilePath = newFilePath

        # Tell the log whats up
        for child in root.iter("filepath"):
            print("Loading " + child.tag + "...")
            print("Standard file path is ", root[0][1].attrib, "\n" + "Custom file path is ", root[0][0].attrib)

        # Get the List back up from the xml and revisit the TXTs so they are what they were on last startup
        createListFiles(self, standardFilePath)
        createTextFiles(newFilePath, 1)

        # Make it work
        activateUi(self.ui)

        # Detect the interactions
        window.addButton.clicked.connect(lambda: addListElement(self))
        window.listWidget.itemSelectionChanged.connect(lambda: updateSelection(self, 0))
        window.listWidget_2.itemSelectionChanged.connect(lambda: updateSelection(self, 1))

        window.actionSetMainFilePath.triggered.connect(lambda: setFilePath(self))
        window.actionStreamHelperDocumentation.triggered.connect(webbrowser.open(""))

        window.updateButton.clicked.connect(lambda: getTextOfItem(self, oldFilePath))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = uiControlTest()
    sys.exit(app.exec_())
    # sys.stdout = old_stdout
