import ctypes
import os
import sys
import webbrowser
from json.decoder import JSONDecodeError

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from qtpy import uic

import resources.images.application_data_images as appim
from resources.access.bindings import initConnection
from resources.runtime import savestate
from resources.runtime.Settings.configfunc import saveConfig, loadConfig
from resources.runtime.Settings.logfunctions import logWrite, logWriteNoTime, logCreate
from resources.runtime.Settings.package import readSettings
from resources.runtime.Settings.program import syncSettings
from resources.runtime.functions import information, createStandardFiles, erroreasy
from resources.runtime.savestate import standardFilePath
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textlists.package import txlinit, addToList, deleteAllItems

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(savestate.APP_ID)
except:
    pass


def is_admin():
    """
    checks whether the user starting the program is an admin. Admin rights are needed for
    locations on other partitions

    :return: bool
    """
    if savestate.platform == "linux":
        return True
    else:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print(e)
            return False


class SettingsWindow(QDialog):
    """
    Settings window to display the settings
    """

    def __init__(self, instance):
        super().__init__(instance)
        self.ui = uic.loadUi(savestate.SOURCE_PATH + 'uis' + savestate.symbol + 'settings.ui')
        self.ui.setWindowTitle("Settings")
        self.ui.treeWidget.expandAll()
        self.ui.stackedSettings.setCurrentIndex(savestate.configList["StartupSettingsTab"])
        syncSettings(self)


class StreamHelper(QMainWindow):
    ui = None

    if is_admin():
        def __init__(self):
            super().__init__()

            # set a window icon

            # self.setWindowIcon(QIcon("images" + savestate.symbol + "icon.png"))

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
            logWriteNoTime("StreamHelper is still under construction! "
                           "Please mind the updates and report any bugs! Thanks!\n")

            information("The Program is in developement! \n"
                        "Please mind the changelog and updates.")

            # Parse the paths from the json files so we know where to check for the files
            try:
                readSettings()
                # print(savestate.configList)
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

            # Tell the log whats up
            print("Loading config data")
            print("Standard file path is ", oldFilePath, "\n" + "Custom file path is ",
                  savestate.configList["CustomFilePath"])
            logWrite("Loading config data")
            logWrite(str(("Standard file path is: " + oldFilePath + "   Custom file path is " +
                          savestate.configList["CustomFilePath"])))

            # Make it work
            window = txlinit(self)
            self.ui = window

            # Basic loading and startup operations
            # initConnection(self)  No API Connections yet, will come in a later update

            # There are only the menu-items connected here in the main package
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
            window.actionVersion_Changes.triggered.connect(lambda:
                                                           webbrowser.open(savestate.SOURCE_PATH + "CHANGELOG.txt"))

            # Load and save settings
            window.actionMain_Settings.triggered.connect(lambda: self.showSettings())

            # Show the credits
            window.actionCredits.triggered.connect(lambda: webbrowser.open(savestate.SOURCE_PATH + "\\images\\common"
                                                                                                   "\\credits.html"))

    else:
        if savestate.platform == 'linux':
            logWrite("The application could not be started in admin mode!")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    def showSettings(self):
        """
        Displays the settings window

        :return: None
        """
        settings = SettingsWindow(self.ui)
        settings.ui.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/images/common/icon2.png"))
    win = StreamHelper()
    app.exec_()
    sys.exit()
