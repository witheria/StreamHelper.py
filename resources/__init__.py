import ctypes
import os
import sys
import webbrowser
from json.decoder import JSONDecodeError

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

from qtpy import uic

import resources.application_data_images as appim
# from resources.access.bindings import initConnection
from resources.runtime import savestate
from resources.runtime.Settings.configfunc import saveConfig, loadConfig
from resources.runtime.Settings.logfunctions import logWrite, logWriteNoTime, logCreate
from resources.runtime.Settings.package import readSettings
from resources.runtime.Settings.program import syncSettings
from resources.runtime.functions import information, createStandardFiles, erroreasy, eSportsExtensionWidget, \
    confirmation
from resources.runtime.savestate import standardFilePath
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textlists.package import txlinit, addToList


def is_admin():
    # checks whether the user starting the program is an admin. Admin rights are needed for
    # locations on other partitions
    if savestate.platform == "linux":
        return True
    else:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print(e)
            return False


class SettingsWindow(QWidget):
    """
    Settings window to display the settings
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(savestate.SOURCE_PATH + 'uis' + savestate.symbol + 'settings.ui')
        self.ui.setWindowTitle("Settings")
        self.ui.treeWidget.expandAll()
        self.ui.stackedSettings.setCurrentIndex(savestate.configList["StartupSettingsTab"])
        syncSettings(self)

    def closeEvent(self, event):
        event.accept()  # let the window close


def showPackageInstaller(parent):

    ok = confirmation("This tool only works on Windows! \n"
                      "Please close OBS Studio for it to work properly!")
    if ok:
        from resources.runtime.Tools.DESPIv3 import Despi
        newWin = QMainWindow(parent)
        Despi(newWin)
        newWin.show()


def showSettings():
    settings = SettingsWindow()
    settings.ui.show()


class StreamHelper(QMainWindow):
    # init the settings window

    # if is_admin(): DEPRECATED: The application does not need admin rights, at least not for everything
    def __init__(self):
        super().__init__()

        # set a window icon and show the early access info

        self.setWindowIcon(QIcon("images" + savestate.symbol + "icon.png"))

        # Check if the folder exists
        if savestate.platform == "linux":
            try:
                print("Trying to create the standard Folder under linux...")
                os.mkdir(savestate.home + "/Documents/StreamHelper")
            except FileExistsError:
                print("Folder exists!")
        else:
            try:
                print("Trying to create the standard Folder under windows...")
                os.mkdir(os.getenv('LOCALAPPDATA') + "\\StreamHelper")
            except FileExistsError:
                print("Folder exists!")

        # Lets create all the standard files (json and txt) or at least check if they exist
        createStandardFiles(0)

        # init a logfile
        logCreate()
        logWrite("The Program is in developement! \n"
                 "Currently, only the textfiles and numbers are working, the other stuff is WIP."
                 "Masks aren't importable yet \n")
        information("The Program is in developement! \n"
                    "Please mind the changelog and updates.")

        # Parse the paths from the xml files so we know where to check for the files
        try:
            readSettings()
            print(savestate.configList)
        except FileNotFoundError:
            print("The config file has not been created yet. Proceeding with standard settings...")
            logWrite("The config file has not been created yet. Proceeding with standard settings...")
        except JSONDecodeError:
            print("There was an error reading the config file! Please try restarting the program. \n"
                  "If this error persists, consider reinstalling or contacting the developer.")
            logWrite("There was an error reading the config file! Please try restarting the program. \n"
                     "If this error persists, consider reinstalling or contacting the developer."
                     "Using Standard Values for now.")
        oldFilePath = savestate.standardFilePath
        newFilePath = savestate.configList["CustomFilePath"]

        # Set the read filepath so we got it internally to work with
        # savestate.standardFilePath = newFilePath

        # Create the timer
        savestate.timer = QTimer()
        savestate.timer.setInterval(1000)
        savestate.timer.start()

        # Tell the log whats up
        print("Loading config data")
        print("Standard file path is ", oldFilePath, "\n" + "Custom file path is ",
              savestate.configList["CustomFilePath"])
        logWrite("Loading config data")
        logWrite(str(("Standard file path is: " + oldFilePath + "   Custom file path is " +
                      savestate.configList["CustomFilePath"])))
        # Make it work

        # Basic loading and startup operations
        window = txlinit(self)

        # Connect the extra window
        savestate.ExtraFieldWidget = eSportsExtensionWidget(self)
        # initConnection(self)

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
        window.actionMain_Settings.triggered.connect(showSettings)

        # Show the bonus Tool
        window.actionPackage_Installer.triggered.connect(lambda: showPackageInstaller(self))

    # else:
    #     if savestate.platform == 'linux':
    #         logWrite("The application could not be started in sudo mode!")
    #    else:
    #        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(savestate.SOURCE_PATH + "/images/common/icon2.png"))
    win = StreamHelper()
    app.exec_()
    # sys.exit(app.exec_())
