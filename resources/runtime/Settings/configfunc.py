import os
import shutil
import xml

from PyQt5.QtWidgets import QFileDialog

from resources.runtime import savestate
from resources.runtime.Settings.perm import getSave
from resources.runtime.functions import information
from resources.runtime.Settings.logfunctions import logWrite, logWriteNoTime
from resources.runtime.textfiles.folderedit import emptyDir

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def saveConfig(self, basefilepath):
    # saves the current lists to a separate file
    filepath = QFileDialog.getSaveFileName(self, "Create Save", basefilepath, ".oi")
    file = str(filepath[0] + ".oi")
    savefile = shutil.copy(str(savestate.standardFilePath + savestate.symbol + "autosave.xml"), file)


def loadConfig(self, basefilepath):
    # Loads a save file
    information("Loading a config file will delete all current contents!")
    file = QFileDialog.getOpenFileName(self, "Open Save", basefilepath, "*.oi")
    self.ui.listWidget.clear()
    self.ui.listWidget_2.clear()
    print(str(file))
    try:
        source = ET.parse(file[0])
        sourceroot = source.getroot()

        logWrite("Trying to parse input file...")

        # delete old textfiles and create a new empty folder
        emptyDir(basefilepath + savestate.symbol + "textfiles")
        os.mkdir(basefilepath + savestate.symbol + "textfiles")
        logWrite("Deleted old textfiles and created a fresh folder!\n")

        # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here,
        # its really quite obvious though. a is the value, b is the name/text the user has called his element,
        # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:
            result = getSave(self, child)
            if result[4] == "text":
                createTextFile(result[2], basefilepath, result[1])
            elif result[4] == "number":
                createTextFile(result[2], basefilepath, str(result[5] + result[1]))

    except xml.etree.ElementTree.ParseError:
        print("No Files found")
        logWrite("No Files found")
    except AttributeError:
        print("File not readable!")
        logWrite("Auto-Save not readable!")
    except FileNotFoundError:
        print("No file selected")
    logWriteNoTime("\n")


def createTextFile(name, path, text):
    # This method is used to create and edit the textfiles used around the program.
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")

    file = open(filename, "w+")
    file.write(text)

    file.close()
