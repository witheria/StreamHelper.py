from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog, QFileDialog, QMainWindow, QTabWidget
from PyQt5 import uic

from resources.runtime import savestate
from resources.runtime.logfunctions import logWrite


def loadMask(self):
    # this function serves the sole purpose to load and save the mask configuration

    # there is no way to create own masks yet, as these need to be loaded into the code
    searchMask = QFileDialog.getOpenFileName(self, "Load Mask", savestate.standardFilePath)
    try:
        file = searchMask[0]
        print(str(file))
        mask = uic.loadUi(file)
        self.ui.tabWidget.addTab(mask, "LoL")
        savestate.masklist[file] = len(savestate.masklist)
        print(savestate.masklist)


    except FileNotFoundError:
        print("No file selected")
