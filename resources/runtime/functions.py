import json
import os
from os.path import exists

from PyQt5.QtCore import QSize
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
    # print("text", retval)
    return retval


def erroreasy(text: str, errorcode: hex):
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


def confirmation(text: str, inputtitle: str = None) -> bool:
    """
    Used to create a confirmation dialog

    :type text: str
    :type inputtitle: str
    :returns: bool
    """
    title = ""
    if inputtitle:
        title = inputtitle
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setText(text)
    if title != "":
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


class eSportsExtensionWidget(QWidget):
    """
    Creates a window with 9 more fields to fill and connects them to the main window
    """
    ui = None

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "eSportsExtensionWidget.ui")
        self.ui.setWindowTitle("More fields...")
        self.setFixedSize(QSize(390, 260))
        self.loadContent()

        self.ui.clearFields.clicked.connect(lambda: self.editField(field="all", value=(False, "")))
        self.ui.saveFields.clicked.connect(lambda: self.saveFields())
        self.ui.funnelFields.clicked.connect(lambda: self.saveFields())

    def editField(self, field: str, value: tuple = (False, "")) -> None:
        """
        Edit a field in the widget.
        There are 9 fields accessible with either "caster", "custom" or "stat" + field number
        Give field = "all" to edit all texts

        E.g.: edit second caster field to value "new": editField(self, "caster2", (True, "new"))

        :param field: contains the line edit to change
        :param value: a tuple containing (whether the field should be funneled, the text the line edit should display)
        :return: None
        """

        if "caster" in field.lower():  # edit a caster field
            if not value == "":  # when these fields are initialized, there is no value
                if field.lower() == "caster1":
                    self.ui.c1Checked.setChecked(value[0])
                    self.ui.Caster1.setText(value[1])
                elif field.lower() == "caster2":
                    self.ui.c2Checked.setChecked(value[0])
                    self.ui.Caster2.setText(value[1])
                elif field.lower() == "caster3":
                    self.ui.c3Checked.setChecked(value[0])
                    self.ui.Caster3.setText(value[1])
                else:
                    print("casterfield overflow error: Give a valid parameter")
        elif "custom" in field.lower():  # edit a custom field
            if not value == "":
                if field.lower() == "custom1":
                    self.ui.cf1Checked.setChecked(value[0])
                    self.ui.Custom1.setText(value[1])
                elif field.lower() == "custom2":
                    self.ui.cf2Checked.setChecked(value[0])
                    self.ui.Custom2.setText(value[1])
                elif field.lower() == "custom3":
                    self.ui.cf3Checked.setChecked(value[0])
                    self.ui.Custom3.setText(value[1])
                else:
                    print("customfield overflow error: Give a valid parameter")
        elif "stat" in field.lower():  # edit a stat field
            if not value == "":
                if field.lower() == "stat1":
                    self.ui.s1Checked.setChecked(value[0])
                    self.ui.Stat1.setText(value[1])
                elif field.lower() == "stat2":
                    self.ui.s2Checked.setChecked(value[0])
                    self.ui.Stat2.setText(value[1])
                elif field.lower() == "stat3":
                    self.ui.s3Checked.setChecked(value[0])
                    self.ui.Stat3.setText(value[1])
                else:
                    print("statfield overflow error: Give a valid parameter")
        elif field.lower() == "all":
            for i in range(1, 4):
                self.editField(str(f"caster{i}"))
                self.editField(str(f"stat{i}"))
                self.editField(str(f"custom{i}"))
        elif field != "Combined":
            print(f"Unknown access parameter {field}")
        else:
            pass

    def getFieldContents(self) -> dict:
        return {
            "Caster1": (self.ui.c1Checked.isChecked(), self.ui.Caster1.text()),
            "Caster2": (self.ui.c2Checked.isChecked(), self.ui.Caster2.text()),
            "Caster3": (self.ui.c3Checked.isChecked(), self.ui.Caster3.text()),
            "Stat1": (self.ui.s1Checked.isChecked(), self.ui.Stat1.text()),
            "Stat2": (self.ui.s2Checked.isChecked(), self.ui.Stat2.text()),
            "Stat3": (self.ui.s3Checked.isChecked(), self.ui.Stat3.text()),
            "Custom1": (self.ui.cf1Checked.isChecked(), self.ui.Custom1.text()),
            "Custom2": (self.ui.cf2Checked.isChecked(), self.ui.Custom2.text()),
            "Custom3": (self.ui.cf3Checked.isChecked(), self.ui.Custom3.text()),
            "Combined": [self.ui.funnelFields.isChecked(), ""]
        }

    def funnelAction(self) -> dict:
        fieldContents = self.getFieldContents()
        fieldContents["Combined"][1] = savestate.configList["funnelfile_separator"].join(
            fieldContents[key][1] for key in fieldContents if fieldContents[key][0] is True and key != "Combined")
        return fieldContents

    def saveFields(self):
        import resources.runtime.textfiles.fileedit as fe
        import resources.runtime.eSports.program as pro
        if self.ui.funnelFields.isChecked():
            savestate.morelist = self.funnelAction()
        else:
            savestate.morelist = self.getFieldContents()
        for key in savestate.morelist:
            fe.initTextFiles("createFile", ["eSports", key, savestate.morelist[key][1], "More fields"])
        pro.saveCurrentState()

    def loadContent(self):
        for key in savestate.morelist:
            self.editField(key, savestate.morelist[key])

    def closeEvent(self, event):
        # dont close the window, just hide it
        self.ui.hide()


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
                # print("Adding item " + key)
                self.ui.select.addItem(key)

    def exec(self):
        ok = self.ui.exec_()
        item = self.ui.select.currentIndex()
        if self.ui.select.itemText(item) == "Number Item":
            item = 1
        elif self.ui.select.itemText(item) == "Text Item":
            item = 0
        elif self.ui.select.itemText(item) == "Chrono Item":
            item = 2
        elif self.ui.select.itemText(item) == "Image Item":
            item = 3
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
