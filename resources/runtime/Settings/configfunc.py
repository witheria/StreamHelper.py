import shutil

from PyQt5.QtWidgets import QFileDialog

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.functions import information
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textlists.package import deleteAllItems

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def saveConfig(self, basefilepath):
    """
    saves the current lists and eSports contents to a save file

    :param self: SettingsWindow
    :param basefilepath: str
    :return: None
    """
    logWrite("Trying to save config, waiting on user...")
    filepath, ok = QFileDialog.getSaveFileName(self, "Create Save", basefilepath, ".oi")
    if ok:
        logWrite("Saving config...")
        file = str(filepath + ".oi")
        try:
            # Just copy the autosave to the user location with a different name lol
            shutil.copy(str(savestate.standardFilePath + savestate.symbol + "autosave.json"), file)
        except FileNotFoundError:
            information("Saving failed, please restart the program!")
            logWrite("Saving failed, please restart the program!")
        print("Exported save to: " + file)


def loadConfig(self, basefilepath):
    """
    This loads a save file with the .oi format for usage in the main program.
    """
    logWrite("Trying to load a config, waiting on user...")
    information("Loading a config file will delete all current contents!")
    file, ok = QFileDialog.getOpenFileName(self, "Open Save", basefilepath, "*.oi")
    if ok:
        logWrite("Loading config file...")
        # print(str(file))
        deleteAllItems()
        print("Opening file from: " + str(file))
        createListFiles(str(file))
