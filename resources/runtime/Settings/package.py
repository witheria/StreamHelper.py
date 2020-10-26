from PyQt5.QtWidgets import QInputDialog
from qtpy import uic

from resources import SettingsWindow
from resources.runtime import savestate
from resources.runtime.functions import information, createStandardFiles
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.savestate import standardFilePath
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textfiles.folderedit import emptyDir

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def setFilePath(self, oldpath):
    # Transition and check interaction function to change the custom filepath parameter
    text, ok = QInputDialog.getText(self, 'Enter Path',
                                    'Enter the desired path for your objects. \nWarning! All Changes since the last '
                                    'Update will be lost!\n \n' +
                                    "Textfiles are at path: " + oldpath)
    logWrite("Filepath change detected. New file path should be " + str(text))
    if len(text) > 0:
        if ":" in text:
            # delete the old textfiles folder so there is no garbage floating around
            emptyDir(oldpath + savestate.symbol + "textfiles")

            setNewFilePath(self, text)

        else:
            information("Make sure the path you enter is valid!")
            logWrite("No valid path entered, exiting...")
    else:
        logWrite("No path entered - nothings changed!")


def setNewFilePath(self, path):
    # initialize the file path and create the standard files at that location
    print(path)
    logWrite("New path for textfiles will be " + str(path))
    createStandardFiles(path, 1)

    logWrite("Created the new textfiles at new path")
    # set the new filepath into the xml document so it gets saved for the next startup
    tree = ET.parse(standardFilePath + savestate.symbol + "config.xml")
    root = tree.getroot()

    root[0][0].set("path", path)
    tree.write(standardFilePath + savestate.symbol + "config.xml")
    print(root[0][0].attrib)

    # reset the two list widgets and reload the items from the xml
    self.ui.listWidget.clear()
    self.ui.listWidget_2.clear()

    createListFiles(self, path)

