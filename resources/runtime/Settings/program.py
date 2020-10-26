
from resources.runtime import savestate
from resources.runtime.functions import erroreasy

activeItem = None


def syncSettings(self):
    # this is a method that's frequently used when opening the settings window. It synchronizes the settings from
    # the file to the QWidget object and the user interface.
    self.ui.treeWidget.itemClicked.connect(lambda: changeSheet(self))

    # self.ui.stackedSettings.setCurrentPage(index)


def changeSheet(self):
    try:
        settingsname = self.ui.treeWidget.currentItem().text(0)
    except TypeError:
        erroreasy(self, "Selected item could not be loaded", 0x0103)

    index = savestate.settingsList[settingsname]
    print("Settings page is now: " + str(index))
    self.ui.stackedSettings.setCurrentIndex(index)

