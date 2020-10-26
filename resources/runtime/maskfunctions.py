from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite


def loadMask(self):
    # this function serves the sole purpose to load and save the mask configuration

    # there is no way to create own masks yet, as these need to be loaded into the code
    searchMask = QFileDialog.getOpenFileName(self, "Load Mask", savestate.standardFilePath)
    try:
        file = searchMask[0]
        files = splitFile(file)

        mask = uic.loadUi(file)
        # if the item is not well formed, the program will try to import it as a basic .ui file
        if len(files) is 1:
            self.ui.tabWidget.addTab(mask, "TestMask")
        else:
            self.ui.tabWidget.addTab(mask, files[0])
        savestate.masklist[file] = len(savestate.masklist)
        print(savestate.masklist)
        self.ui.tabWidget.setCurrentWidget(mask)

    except FileNotFoundError:
        print("No Mask file selected")


def splitFile(filepath):
    # this method splits the custom filetype into a .py and a .oic file
    pack = open(filepath, "r")
    packtext = pack.read()
    files = packtext.split("&&")
    print(len(files))
    if len(files) is 1:
        return files
    else:
        logWrite("The Mask included in this file is " + str(files[0]))
        file1 = open(savestate.standardFilePath + savestate.symbol + str(files[0]) + ".py", "w+")
        file1.write(files[1])
        file2 = open(savestate.standardFilePath + savestate.symbol + str(files[0]) + ".oic", "w+")
        file2.write(files[2])
        file1.close()
        file2.close()

    pack.close()
    return files
