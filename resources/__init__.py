import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from qtpy import QtGui, uic

from resources.runtime import savestate
from resources.runtime.Settings.configfunc import saveConfig, loadConfig
from resources.runtime.functions import information, createStandardFiles, erroreasy
from resources.runtime.Settings.logfunctions import logWrite, logWriteNoTime, logCreate
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textlists.package import txlinit, addToList

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from resources.runtime.savestate import standardFilePath

import webbrowser

import ctypes
import sys


def is_admin():
    # checks whether the user starting the program is an admin. Admin rights are needed for
    # locations on other partitions
    if savestate.platform == "linux":
        return True
    else:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


class SettingsWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('uis' + savestate.symbol + 'settings.ui')
        self.ui.setWindowTitle("Spoon")


class StreamHelper(QMainWindow):
    if is_admin():
        def __init__(self):
            super().__init__()

            # init the settings window
            self.w = None  # No external window yet

            # set a window icon and show the early access info

            self.setWindowIcon(QIcon("images" + savestate.symbol + "icon.png"))
            information("The Program is in developement! \n"
                        "Currently, only the textfiles and numbers are working, the other stuff is WIP. . Masks aren't "
                        "importable yet")

            # Check if the folder exists
            if savestate.platform == "linux":
                try:
                    print("Trying to create the standard Folder...")
                    os.mkdir(savestate.home + "/Documents/StreamHelper")
                except FileExistsError:
                    print("Folder exists!")
            else:
                try:
                    print("Trying to create the standard Folder...")
                    os.mkdir(os.getenv('LOCALAPPDATA') + "\\StreamHelper")
                except FileExistsError:
                    print("Folder exists!")

            # Lets create all the standard files (xml and txt) or at least check if they exist
            createStandardFiles(standardFilePath, 0)

            # init a logfile
            logCreate()
            logWrite("The Program is in developement! \n"
                     "            Currently, only the textfiles and numbers are working, the other stuff is WIP. "
                     "Masks aren't "
                     "importable yet \n")

            # Parse the paths from the xml files so we know where to check for the files
            tree = ET.parse(standardFilePath + savestate.symbol + "config.xml")
            root = tree.getroot()
            dictStandard = root[0][1].attrib
            dictCustom = root[0][0].attrib

            oldFilePath = dictStandard["path"]
            newFilePath = dictCustom["path"]

            # Set the read filepath so we got it internally to work with
            # savestate.standardFilePath = newFilePath

            # Tell the log whats up
            for child in root.iter("filepath"):
                print("Loading " + child.tag + "...")
                print("Standard file path is ", root[0][1].attrib, "\n" + "Custom file path is ", root[0][0].attrib)
                logWrite(str("Loading " + child.tag + "..." + "\n"))
                logWrite(str("Standard file path is " + str(root[0][1].attrib["path"]) + "\n" +
                             "            Custom file path is " + str(root[0][0].attrib["path"]) + "\n"))

            # Make it work

            # Basic loading and startup operations
            window = txlinit(self, newFilePath, oldFilePath)

            # Detect the interactions / NOW HANDLED IN DESIGNATED PACKAGES
            # There are only the menu-items binded here in the main package

            # This will be deprecated soon, moved to settings
            # window.actionSetMainFilePath.triggered.connect(lambda: setFilePath(self, newFilePath))
            # Show the documentation (links to online though)
            window.actionStreamHelperDocumentation.triggered.connect(
                lambda: webbrowser.open("https://github.com/xFLLSquadronNorden/StreamHelper.py"))
            # Save and Load configs from files
            window.actionSave.triggered.connect(lambda: saveConfig(self, newFilePath))
            window.actionLoad.triggered.connect(lambda: loadConfig(self, newFilePath))
            # Quit the application
            window.actionQuit.triggered.connect(lambda: sys.exit(0))

            window.actionLog.triggered.connect(lambda: webbrowser.open(standardFilePath + savestate.symbol +
                                                                       "StreamLog.log"))
            # Show the new version Changes
            window.actionVersion_Changes.triggered.connect(lambda: webbrowser.open("CHANGELOG.txt"))

            # Load and save settings
            window.actionMain_Settings.triggered.connect(self.showSettings)

        def showSettings(self):
            if self.w is None:
                self.w = SettingsWindow()
                self.w.ui.show()

            else:
                self.w.close()  # Close window.
                self.w = None  # Discard reference.
    else:
        if savestate.platform is 'linux':
            logWrite("The application could not be started in sudo mode!")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.ico"))
    win = StreamHelper()
    app.exec_()
    # sys.exit(app.exec_())
