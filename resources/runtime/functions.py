import os
from os.path import exists

from PyQt5.QtWidgets import QMessageBox, QListWidget

from resources.runtime import savestate
from resources.runtime.savestate import standardFilePath, standardFileNames, standardXMLNames

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def activateUi(self):
    """

    :type self: QMainWindow
    """
    self.listWidget.setSelectionMode(QListWidget.ExtendedSelection)
    self.listWidget_2.setSelectionMode(QListWidget.ExtendedSelection)


def updateSelection(self, number, *row):
    # DEPRECATED
    savestate.lastListSelected = number
    print("Last list selected: " + str(savestate.lastListSelected))

    if number == 0:
        i = self.ui.listWidget.currentRow()
        current = self.ui.listWidget.currentItem()

        savestate.lastItemSelected[1] = i
        w = self.ui.listWidget.itemWidget(current).checkBox.setChecked(True)

        alloydeselectItem(self)
        print("Selected Item: " + str(i) + " in List 1")

    elif number == 1:
        i = self.ui.listWidget_2.currentRow()
        current = self.ui.listWidget_2.currentItem()

        savestate.lastItemSelected[1] = i
        w = self.ui.listWidget_2.itemWidget(current).checkBox.setChecked(True)

        alloydeselectItem(self)
        print("Selected Item: " + str(i) + " in List 2")


def alloydeselectItem(self):
    # UNUSED SINCE DEPRECATED!
    if self.ui.addright.isChecked():
        savestate.lastListSelected = 1
    if not savestate.deselectListFunctionInitiated:
        savestate.deselectListFunctionInitiated = True

    else:

        if savestate.lastListSelected == 0:
            if not savestate.deselectItemFunctionInitiated[0]:
                savestate.deselectItemFunctionInitiated[0] = True
            else:
                current = self.ui.listWidget.item(savestate.lastItemSelected[0])
                w = self.ui.listWidget.itemWidget(current).checkBox.setChecked(False)

                savestate.lastItemSelected[0] = savestate.lastItemSelected[1]

        elif savestate.lastListSelected == 1:
            if not savestate.deselectItemFunctionInitiated[1]:
                savestate.deselectItemFunctionInitiated[1] = True
            else:
                current = self.ui.listWidget_2.item(savestate.lastItemSelected[0])
                w = self.ui.listWidget_2.itemWidget(current).checkBox.setChecked(False)

                savestate.lastItemSelected[0] = savestate.lastItemSelected[1]
        else:
            erroreasy("No List Widget was initiated!", 0o02)


def resetFiles():
    # TODO: Get on with it
    pass


def saveListState():
    # TODO: Get on with it #2
    pass


def information(text):
    w = QMessageBox()
    w.setText(text)
    w.setIcon(QMessageBox.Information)
    w.setStandardButtons(QMessageBox.Ok)
    w.setWindowTitle("Information")

    retval = w.exec_()
    print("text", retval)


def erroreasy(self, text, errorcode):
    w = QMessageBox()
    w.setText(text)
    w.setIcon(QMessageBox.Information)
    w.setStandardButtons(QMessageBox.Ok)
    w.setWindowTitle("Error")

    retval = w.exec_()
    print("text", retval, errorcode)


def initXMLFiles(path):
    for file in standardXMLNames:
        print("Opening files at " + path + "\\" + file + ".xml")
        open(path + "\\" + file + ".xml", "w+")

    data = ET.Element('data')
    filepath = ET.SubElement(data, "filepath")
    customfilepath = ET.SubElement(filepath, "CustomFilePath")
    standardFilePathXML = ET.SubElement(filepath, "StandardFilePath")
    customfilepath.set("path", standardFilePath)
    standardFilePathXML.set("path", standardFilePath)
    myfile = open(standardFilePath + "\\" + "config.xml", "w")
    myfile.write(ET.tostring(data).decode('utf-8'))


def createStandardFiles(path, arg):
    print("Trying to create the standard Files with arg " + str(arg) + "...")
    try:
        os.mkdir(path + "\\textfiles")
    except FileExistsError:
        print("Standard file folder exists!")

    if arg == 0:
        if exists(path + "\\config.xml"):
            print("XML Files exist, not creating any new ones")
        else:
            initXMLFiles(path)

    else:
        print("Only creating textfiles...")
        createTextFiles(path, 1)


def createTextFiles(path, *arg, **name):
    if arg == 0:
        open(path + "\\textfiles" + "\\" + name + ".txt", "w+")
        print(name, " initialized!")

    else:
        for i in standardFileNames:
            if exists(path + "\\textfiles" + "\\" + i + ".txt"):
                print(i + " already exists!")
            else:
                open(path + "\\textfiles" + "\\" + i + ".txt", "w+")
                print(i + " initialized!")


def setNewFilePath(path):
    # initialize the file path and create the standard files at that location
    print(path)
    createStandardFiles(path, 1)

    # set the new filepath into the xml document so it gets saved for the next startup
    tree = ET.parse(standardFilePath + "\\config.xml")
    root = tree.getroot()

    root[0][0].set("path", path)
    tree.write(standardFilePath + "\\config.xml")
    print(root[0][0].attrib)
