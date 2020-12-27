import webbrowser

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.Settings.package import updateSettings
from resources.runtime.functions import erroreasy, createStandardFiles
from resources.runtime.textfiles.fileedit import initTextFiles
from resources.runtime.textfiles.folderedit import emptyDir
from resources.runtime.textlists.package import updateLists

activeItem = None


def syncSettings(self):
    """
    this is a method that's frequently used when opening the settings window. It synchronizes the settings from
    the file to the QWidget object and the user interface.
    :param self: SettingsWindow
    :return: None
    """
    logWrite("Trying to load up the settings window...")
    self.ui.treeWidget.itemClicked.connect(lambda: changeSheet(self))
    # File Path options
    self.ui.changeTextPath.clicked.connect(lambda: changeTextPath(self))
    self.ui.standardPath.setText(savestate.standardFilePath)
    self.ui.TextFilePath.setText(savestate.configList["CustomFilePath"])

    self.ui.infoReset.hide()

    self.ui.logoButton.setIcon(QIcon(":/images/common/icon2.png"))
    self.ui.logoButton.setIconSize(QSize(64, 64))
    self.ui.logoButton.clicked.connect(lambda:
                                       webbrowser.open("https://www.paypal.com/donate?hosted_button_id=825RPFTRDCW7A"))

    # Lists
    if self.ui.allowText.isChecked():
        savestate.configList["AllowedItems"]["Text Item"] = True
    if self.ui.allowNumbers.isChecked():
        savestate.configList["AllowedItems"]["Number Item"] = True

    self.ui.SplitLists.setChecked(savestate.configList["ListSplit"])
    self.ui.SplitLists.stateChanged.connect(lambda: activateFolderSplitting(self.ui.SplitLists))

    self.ui.AutoUpdate.setChecked(savestate.configList["AutoUpdateFiles"])
    self.ui.AutoUpdate.stateChanged.connect(lambda: autoUpdateFiles(self))

    self.ui.llistname.setText(savestate.configList["LeftListName"])
    self.ui.rlistname.setText(savestate.configList["RightListName"])
    self.ui.llistname.editingFinished.connect(lambda: changeListName(self, 1))
    self.ui.rlistname.editingFinished.connect(lambda: changeListName(self, 0))
    self.ui.resetSettings.clicked.connect(lambda: resetSettings(self))


def changeSheet(self):
    """
    This method is used to synchronize the item-changing in the QTreeWidget of the settings with the stacked widget


    :param self: SettingsWindow
    :return: None
    """
    settingsname = None

    try:
        settingsname = self.ui.treeWidget.currentItem().text(0)
    except TypeError:
        erroreasy("Selected item could not be loaded", 0x0103)

    index = savestate.settingsList[settingsname]
    print("Settings page is now: " + str(index))
    self.ui.stackedSettings.setCurrentIndex(index)


def changeTextPath(self):
    """
    This method changes the textfilepath used around the program

    :param self: SettingsWindow
    :return: None
    """
    logWrite("Trying to change the text path...")
    directory = QFileDialog.getExistingDirectory(self, "Change text file path",
                                                 savestate.configList["CustomFilePath"],
                                                 QFileDialog.DontResolveSymlinks)
    logWrite("The given path is: " + directory)
    if ":" or "/" in directory:
        emptyDir(savestate.configList["CustomFilePath"] + savestate.symbol + "textfiles")
        self.ui.TextFilePath.setText(directory)
        savestate.configList["CustomFilePath"] = directory
        print("Filepath changed to: " + directory)
        createStandardFiles(1)
        updateSettings()
        updateLists()
        initTextFiles("initFolders")
    else:
        logWrite("The path is not valid!")
        erroreasy("Please give a valid filepath!", 0x0304)


def activateFolderSplitting(checkbox):
    """
    Used to create a folder for each list if the setting is changed while in the program

    :type checkbox: QCheckBox
    :return: None
    """
    savestate.configList["ListSplit"] = checkbox.isChecked()
    logWrite("List split has been set to: " + str(savestate.configList["ListSplit"]))
    updateSettings()
    createStandardFiles(1)
    initTextFiles("initFolders")
    updateLists()


def autoUpdateFiles(self):
    """
    Enables Auto-Updating of the textfiles. This means, that when the cursor focus on the lineedit within a list item
    is lost, the textfile updates automatically without user interaction

    :param self: SettingsWindow
    :return: None
    """
    print("Auto updating files is set to ", str(self.ui.AutoUpdate.isChecked()))
    savestate.configList["AutoUpdateFiles"] = self.ui.AutoUpdate.isChecked()
    logWrite("Auto-Updating has been set to: " + str(savestate.configList["AutoUpdateFiles"]))
    updateSettings()
    updateLists()


def changeListName(self, listwidget):
    """
    Used to change the name of a list and the folder it creates
    Returns True if the name has been changed successfully

    :param self: SettingsWindow
    :param listwidget: int
    :return: bool
    """

    if listwidget == 0:  # List Right
        savestate.configList["RightListName"] = self.ui.rlistname.text()
        print("Changing name of the right list to " + self.ui.rlistname.text())
        logWrite("Changing name of the right list to " + self.ui.rlistname.text())
    elif listwidget == 1:  # List Left
        savestate.configList["LeftListName"] = self.ui.llistname.text()
        print("Changing name of the left list to " + self.ui.llistname.text())
        logWrite("Changing name of the left list to " + self.ui.llistname.text())
    savestate.saveLists["Left"].setToolTip(savestate.configList["LeftListName"])
    savestate.saveLists["Right"].setToolTip(savestate.configList["RightListName"])
    updateSettings()
    initTextFiles("initFolders")
    updateLists()


def resetSettings(self):
    """
    Used to reset the settings to standard values

    :param self: SettingsWindow
    :return: None
    """
    logWrite("Trying to reset the setting to standard...")
    savestate.configList = savestate.standardConfigList
    updateSettings()
    self.ui.infoReset.show()
