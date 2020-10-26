import os
from os.path import exists

from PyQt5.QtWidgets import QMessageBox

from resources.runtime import savestate
from resources.runtime.savestate import standardFilePath, standardXMLNames
from resources.runtime.Settings.logfunctions import logWrite

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


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
    print(text, retval, errorcode)
    logWrite(text + ", " + str(retval) + ", " + str(errorcode))


def createStandardFiles(path, arg):
    print("Trying to create the standard Files with arg " + str(arg) + "...")
    try:
        os.mkdir(path + savestate.symbol + "textfiles")
    except FileExistsError:
        print("Standard file folder exists!")

    if arg == 0:
        if exists(path + savestate.symbol + "config.xml"):
            print("XML Files exist, not creating any new ones")
        else:
            initXMLFiles(path)

    else:
        print("Not valid!")


def initXMLFiles(path):
    for file in standardXMLNames:
        print("Opening files at " + path + savestate.symbol + file + ".xml")
        open(path + savestate.symbol + file + ".xml", "w+")

    data = ET.Element('data')
    filepath = ET.SubElement(data, "filepath")
    customfilepath = ET.SubElement(filepath, "CustomFilePath")
    standardFilePathXML = ET.SubElement(filepath, "StandardFilePath")
    customfilepath.set("path", standardFilePath)
    standardFilePathXML.set("path", standardFilePath)
    myfile = open(standardFilePath + savestate.symbol + "config.xml", "w")
    myfile.write(ET.tostring(data).decode('utf-8'))