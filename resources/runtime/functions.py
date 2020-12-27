import json
import os
from os.path import exists

from PyQt5.QtWidgets import QMessageBox, QWidget
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.savestate import standardXMLNames


def information(text):
    logWrite("Information: " + text)
    w = QMessageBox()
    w.setText(text)
    w.setIcon(QMessageBox.Information)
    w.setStandardButtons(QMessageBox.Ok)
    w.setWindowTitle("Information")

    retval = w.exec_()
    print("text", retval)
    return retval


def erroreasy(text, errorcode):
    """
    Used to create an error dialog, usually for smaller errors
    :param text: str
    :param errorcode: hex
    :return: None
    """
    w = QMessageBox()
    w.setText(text)
    w.setIcon(QMessageBox.Information)
    w.setStandardButtons(QMessageBox.Ok)
    w.setWindowTitle("Error")

    retval = w.exec_()
    print(text, retval, errorcode)
    logWrite(text + ", " + str(retval) + ", " + str(errorcode))


def confirmation(text: str, *title: str) -> bool:
    """
    Used to create a confirmation dialog

    :type text: str
    :type title: str
    :returns: bool
    """
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setText(text)
    if title is str:
        dialog.setWindowTitle(title)
    else:
        dialog.setWindowTitle("Warning")
    dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    yes = dialog.exec_()
    result = None
    if yes == QMessageBox.Ok:
        result = True
    if yes == QMessageBox.Cancel:
        result = False
    return result


class itemSelect(QWidget):
    """
    Item selection Dialog to select items
    """
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "SelectionDialog.ui")
        self.ui.setWindowTitle("Item Selection")
        self.ui.buttonBox.accepted.connect(self.ui.accept)
        self.ui.buttonBox.rejected.connect(self.ui.reject)
        for key in savestate.configList["AllowedItems"]:
            if savestate.configList["AllowedItems"][key]:
                self.ui.select.addItem(key)

    def exec(self):
        ok = self.ui.exec_()
        item = self.ui.select.currentIndex()
        if self.ui.select.itemText(item) == "Number Item":
            item = 1
        elif self.ui.select.itemText(item) == "Text Item":
            item = 0
        text = self.ui.name.text()
        return ok, item, text


def createStandardFiles(arg):
    print("Trying to create the standard files with arg " + str(arg) + "...")
    try:
        os.mkdir(savestate.standardFilePath)
    except FileExistsError:
        print("Standard folder exists...")

    basepath = savestate.configList["CustomFilePath"] + savestate.symbol + "textfiles" + savestate.symbol
    for key in savestate.standardDirNames:
        try:
            os.makedirs(basepath + key)
        except FileExistsError:
            # print(key + " exists!")
            pass
    if savestate.configList["ListSplit"]:
        try:
            os.mkdir(basepath + "Lists" + savestate.symbol + savestate.configList["RightListName"])
            os.mkdir(basepath + "Lists" + savestate.symbol + savestate.configList["LeftListName"])
            print("List splitting enable and folders created!")
        except FileExistsError:
            print("List splitting enabled and folders exist...")
    if arg == 0:
        if exists(savestate.standardFilePath + savestate.symbol + "config.json"):
            print("JSON Files exist, not creating any new ones")
        else:
            initJSONFiles(savestate.standardFilePath)

    else:
        print("Not valid!")


def initJSONFiles(path):
    logWrite("Initializing standard files...")
    for file in standardXMLNames:
        print("Opening files at " + path + savestate.symbol + file + ".json")
        data = open(path + savestate.symbol + file + ".json", "w+")
        if file == "config":
            arr = json.dumps(savestate.configList, indent=4)
            data.write(arr)
            data.close()
        if file == "autosave":
            arr = json.dumps(savestate.autosave_standard, indent=4)
            data.write(arr)
            data.close()
