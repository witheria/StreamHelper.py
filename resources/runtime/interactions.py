import os
import shutil
import xml
from os.path import join

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog, QFileDialog, QMainWindow
from qtpy import uic

from resources import information
from resources.runtime import savestate
from resources.runtime.functions import logWrite, logWriteNoTime, createStandardFiles
from resources.runtime.savestate import standardFilePath

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def addListElement(self):
    # Add an element to one of the lists with full user interaction.

    # text, ok = QInputDialog.getText(self, 'Enter Name',
    # 'Enter the desired name for your object:')
    itemselect = uic.loadUi("uis" + savestate.symbol + "SelectionDialog.ui")
    itemselect.setWindowTitle("Itemselection")
    itemselect.buttonBox.accepted.connect(itemselect.accept)
    itemselect.buttonBox.rejected.connect(itemselect.reject)
    ok = itemselect.exec_()
    item = itemselect.select.currentIndex()
    text = itemselect.name.text()

    print(ok)

    if item == 1:
        # Creates a NUMBER
        if ok:
            createNumberItem(self, text, 0, 3, "")
            savestate.itemorder.append(savestate.itemType.NUMBER)
    elif item == 0:
        # Creates a TEXT Item
        if ok:
            createTextItem(self, text, "", 3)
            savestate.itemorder.append(savestate.itemType.TEXT)
    elif item == 2:
        # Creates a CERTAINTEXT Item which allows the user to input a number of texts and change them at will
        if ok:
            information("Not implemented yet!")
            # savestate.itemorder.append(savestate.itemType.CERTAINTEXT) TODO
    elif item == 3:
        # Creates a CHRONOS item which writes time or dates to textfiles
        if ok:
            createChronoItem(self, text, "", 3)
            # savestate.itemorder.append(savestate.itemType.CHRONOS) TODO


def createTextItem(self, text, value, slist):
    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2
    if self.ui.addright.isChecked() or slist == 1:

        savestate.count = rightOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        logWrite("Added item: " + str(item[savestate.count]) + "\n")

        wid = uic.loadUi("uis" + savestate.symbol + "TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        if value:
            wid.lineEdit.setText(value)
        wid.setWhatsThis("text")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, savestate.count + 1)
        item[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(item[savestate.count])
        rightOne.setItemWidget(item[savestate.count], wid)

    elif self.ui.addleft.isChecked() or slist == 0:
        savestate.count = leftOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        wid = uic.loadUi("uis" + savestate.symbol + "TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)
        if value:
            wid.lineEdit.setText(value)
        wid.setWhatsThis("text")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, text)
        item[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(item[savestate.count])
        leftOne.setItemWidget(item[savestate.count], wid)

    else:
        information("Please select a list to add the object!")


def createNumberItem(self: QMainWindow, text: str, value: int, listnr: int, pretext: str) -> None:
    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2

    if listnr == 0 or self.ui.addleft.isChecked():
        savestate.count = leftOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        wid = uic.loadUi("uis" + savestate.symbol + "NumberWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        wid.spinBox.setValue(int(value))

        wid.lineEdit.setText(pretext)

        wid.setWhatsThis("number")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, text)
        item[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(item[savestate.count])
        leftOne.setItemWidget(item[savestate.count], wid)

    elif listnr == 1 or self.ui.addright.isChecked():

        savestate.count = rightOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))

        wid = uic.loadUi("uis" + savestate.symbol + "NumberWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        wid.lineEdit.setText(pretext)

        wid.spinBox.setValue(int(value))

        wid.setWhatsThis("number")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, savestate.count + 1)
        item[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(item[savestate.count])
        rightOne.setItemWidget(item[savestate.count], wid)

    else:
        information("Please select a list to add the object!")


def createChronoItem(self, text, value, listnr):
    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2

    if listnr == 0 or self.ui.addleft.isChecked():
        savestate.count = leftOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        wid = uic.loadUi("uis" + savestate.symbol + "ChronoWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        wid.showTime.setText(value)

        wid.setWhatsThis("chrono")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, text)
        item[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(item[savestate.count])
        leftOne.setItemWidget(item[savestate.count], wid)

    elif listnr == 1 or self.ui.addright.isChecked():

        savestate.count = rightOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))

        wid = uic.loadUi("uis" + savestate.symbol + "ChronoWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        wid.showTime.setText(value)

        wid.setWhatsThis("chrono")
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, savestate.count + 1)
        item[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(item[savestate.count])
        rightOne.setItemWidget(item[savestate.count], wid)

    else:
        information("Please select a list to add the object!")


def autTextListElement(self, name, nr, value, *itemType):
    """

    :param self: QMainWindow
    :param name: String
    :param nr: Integer
    :param value: String
    :param itemType: Integer
    """
    # Let the program add elements with values entered into the function. Differs from addListElement, since it needs
    # no user input

    # This conversion is just, so I can tell the difference easier, nothing really
    text = name

    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2

    # Here we check which list the item needs to be put into. 0 is left 1 is right
    if nr == 1:

        # add the item to the dictionary so we can keep track of it
        savestate.count = rightOne.count()
        dictname = {savestate.count: str(text)}
        print("Added item: " + str(dictname.get(savestate.count)) + "\n")

        # create the widget and set the text
        wid = uic.loadUi("uis" + savestate.symbol + "TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        # insert the value
        wid.lineEdit.setText(value)

        # add the item to the list
        # (DEPRECATED) print(dictname[savestate.count])
        dictname[savestate.count] = QListWidgetItem()
        dictname[savestate.count].setFlags(dictname[savestate.count].flags() | Qt.ItemIsEditable)
        dictname[savestate.count].setData(5, savestate.count + 1)
        dictname[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(dictname[savestate.count])
        rightOne.setItemWidget(dictname[savestate.count], wid)
    elif nr == 0:
        # do the same
        savestate.count = leftOne.count()
        dictname = {savestate.count: str(text)}
        print("Added item: " + str(dictname.get(savestate.count)) + "\n")
        wid = uic.loadUi("uis" + savestate.symbol + "TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)
        wid.lineEdit.setText(value)
        dictname[savestate.count] = QListWidgetItem()
        dictname[savestate.count].setFlags(dictname[savestate.count].flags() | Qt.ItemIsEditable)
        dictname[savestate.count].setData(5, text)
        dictname[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(dictname[savestate.count])
        leftOne.setItemWidget(dictname[savestate.count], wid)
    else:
        # deprecated
        information("Please select a list to add the object!")


def getTextOfItem(self, path, altpath, *item):
    # This function gets the text from within the List Widgets, first from the left list, then from the other one it
    # will also write these texts into the xml and text files. If there is an item given it will internally return
    # that item in the form: "text" #unique "label" so it can be split. item should be a number

    # init the xml file for the textfiles
    xmlFile = open(path + savestate.symbol + "autosave.xml", "w+")

    # Introducing the xml data tree
    data = ET.Element('data')
    itemdirect = {}

    # We want one for every list (2)
    for index in range(0, self.ui.listWidget.count()):
        # Get the current element on index
        current = self.ui.listWidget.item(index)

        # Save the label that is customizable

        label = self.ui.listWidget.itemWidget(current).label.text()

        # Create the XML Tree element
        itemdirect[index] = ET.SubElement(data, ("item" + str(index)))

        # Save the type of the item
        itemtype = str(self.ui.listWidget.itemWidget(current).whatsThis())
        Listtype = ET.SubElement(itemdirect[index], "itemtype")
        Listtype.set("itemtype", itemtype)
        print(itemtype)

        if itemtype == "text":
            # Set the list in which the item lays for revive purposes
            listnr = ET.SubElement(itemdirect[index], "list")
            listnr.set("list", "0")
            # Now the value of the item
            text = self.ui.listWidget.itemWidget(current).lineEdit.text()
            value1 = ET.SubElement(itemdirect[index], "value")
            value1.set("value", text)
            # And now the label
            labeltext = ET.SubElement(itemdirect[index], "labeltext")
            labeltext.set("text", label)

            # create the textfile associated with the element
            createTextFile(label, altpath, text)

        if itemtype == "number":
            # Set the list in which the item lays for revive purposes
            listnr = ET.SubElement(itemdirect[index], "list")
            listnr.set("list", "0")
            # Now the values of the item
            valueint = str(self.ui.listWidget.itemWidget(current).spinBox.value())

            value = ET.SubElement(itemdirect[index], "value")
            value.set("value", valueint)

            textvaluestr = self.ui.listWidget.itemWidget(current).lineEdit.text()

            textvalue = ET.SubElement(itemdirect[index], "textvalue")
            textvalue.set("textvalue", textvaluestr)

            # And now the label
            labeltext = ET.SubElement(itemdirect[index], "labeltext")
            labeltext.set("text", label)

            # create the textfile associated with the element
            createTextFile(label, altpath, str(textvaluestr + valueint))

        # Out to the log it goes
        print("text of item", itemdirect[index], "saved to file")

        # List 2

    for index in range(0, self.ui.listWidget_2.count()):
        # Get the current element on index
        current = self.ui.listWidget_2.item(index)

        # Save the label that is customizable

        label = self.ui.listWidget_2.itemWidget(current).label.text()

        # Create the XML Tree element
        itemdirect[index] = ET.SubElement(data, ("item" + str(index)))

        # Save the type of the item
        itemtype = str(self.ui.listWidget_2.itemWidget(current).whatsThis())
        Listtype = ET.SubElement(itemdirect[index], "itemtype")
        Listtype.set("itemtype", itemtype)
        print(itemtype)

        if itemtype == "text":
            # Set the list in which the item lays for revive purposes
            listnr = ET.SubElement(itemdirect[index], "list")
            listnr.set("list", "1")
            # Now the value of the item
            text = self.ui.listWidget_2.itemWidget(current).lineEdit.text()
            value1 = ET.SubElement(itemdirect[index], "value")
            value1.set("value", text)
            # And now the label
            labeltext = ET.SubElement(itemdirect[index], "labeltext")
            labeltext.set("text", label)

            # create the textfile associated with the element
            createTextFile(label, altpath, text)

        if itemtype == "number":
            # Set the list in which the item lays for revive purposes
            listnr = ET.SubElement(itemdirect[index], "list")
            listnr.set("list", "1")
            # Now the values of the item
            valueint = str(self.ui.listWidget_2.itemWidget(current).spinBox.value())

            value = ET.SubElement(itemdirect[index], "value")
            value.set("value", valueint)

            textvaluestr = self.ui.listWidget_2.itemWidget(current).lineEdit.text()

            textvalue = ET.SubElement(itemdirect[index], "textvalue")
            textvalue.set("textvalue", textvaluestr)

            # And now the label
            labeltext = ET.SubElement(itemdirect[index], "labeltext")
            labeltext.set("text", label)

            # create the textfile associated with the element
            createTextFile(label, altpath, str(textvaluestr + valueint))

        # Out to the log it goes
        print("text of item", itemdirect[index], "saved to file")
    xmlFile.write(ET.tostring(data).decode("utf-8"))

    # If there's an item given we might want to output this
    if item == int:
        try:
            return self.ui.listWidget.item(item).lineEdit.text(), "#unique", self.ui.listWidget.item(6).label.text()

        except TypeError:
            print("Didnt find item in list 1...")
        try:
            return self.ui.listWidget_2.item(item).lineEdit.text(), "#unique", self.ui.listWidget_2.item(
                item).label.text()
        except TypeError:
            print("Requested item could not be located!")


def createListFiles(self, newpath):
    # This method recreates the list files from the autosave.xml file.
    # It determines which kind of item has to be created

    print("Trying to recall what was in the list...")
    logWrite("Trying to recall what was in the list...")

    # delete old textfiles and create a new empty folder
    emptyDir(newpath + savestate.symbol + "textfiles")
    os.mkdir(newpath + savestate.symbol + "textfiles")
    logWrite("Deleted old textfiles and created a fresh folder!\n")

    # Lets look in the xml so we know what was up
    try:
        print(savestate.standardFilePath)
        source = ET.parse(savestate.standardFilePath +  savestate.symbol + "autosave.xml")
        sourceroot = source.getroot()
        logWrite("Parsing autosave...")

        # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here.
        # a is the value, b is the name/text the user has called his element,
        # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:

            a = child.find("value").attrib.get("value")
            b = child.find("labeltext").attrib.get("text")
            c = int(child.find("list").attrib.get("list"))
            d = child.find("itemtype").attrib.get("itemtype")

            try:
                e = child.find("textvalue").attrib.get("textvalue")
                print("Number Item")
            except AttributeError:
                print("Text Item")
                e = ""

            # x = next(iter(a.values()))

            print(
                "# Value of the " + str(d) + " item is " + str(a) + "\n" + "# Name of item is " + str(
                    b) + "\n" + "# List where it needs to be is " +
                str(c))
            logWriteNoTime("\n# Value of the " + str(d) + " item is " + str(a) + "\n" +
                           "# Name of item is " + str(b) + "\n" +
                           "# List where it needs to be is " + str(c) + "\n")

            if d == "text":
                createTextItem(self, b, a, int(c))
                createTextFile(b, newpath, a)
            elif d == "number":
                createNumberItem(self, b, a, int(c), e)
                createTextFile(b, newpath, str(e + a))
            else:
                information("The Element could not be loaded! The data may have been corrupted!")
                logWrite("The Element could not be loaded! The data may have been corrupted!")
    except xml.etree.ElementTree.ParseError:
        print("No Files found")
        logWrite("No Files found")
    except AttributeError:
        print("File not readable!")
        logWrite("Autosave not readable!")

    logWriteNoTime("\n")


def createTextFile(name, path, text):
    # This method is used to create and edit the textfiles used around the program.
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")

    file = open(filename, "w+")
    file.write(text)

    file.close()


def deleteTextFile(name, path):
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")
    os.remove(filename)


def emptyDir(path):
    try:
        shutil.rmtree(join(path))
    except FileNotFoundError:

        logWrite("The folder could not be found!")


'''
    def autListElement(self, name, nr, value, itemType):
        if itemType == "text":
            createTextItem(self, name, value, nr)
        elif itemType == "number":
            createNumberItem(self, name, value, nr)
        else:
            print("Not a valid Item!")
'''


def saveConfig(self, basefilepath):
    # saves the current lists to a separate file
    filepath = QFileDialog.getSaveFileName(self, "Create Save", basefilepath, ".oi")
    file = str(filepath[0] + ".oi")
    savefile = shutil.copy(str(savestate.standardFilePath + savestate.symbol + "autosave.xml"), file)


def loadConfig(self, basefilepath):
    # Loads a save file
    file = QFileDialog.getOpenFileName(self, "Open Save", basefilepath, "*.oi")
    self.ui.listWidget.clear()
    self.ui.listWidget_2.clear()
    print(str(file))
    try:
        source = ET.parse(file[0])
        sourceroot = source.getroot()

        logWrite("Trying to parse input file...")

        # delete old textfiles and create a new empty folder
        emptyDir(basefilepath + savestate.symbol + "textfiles")
        os.mkdir(basefilepath + savestate.symbol + "textfiles")
        logWrite("Deleted old textfiles and created a fresh folder!\n")

        # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here,
        # its really quite obvious though. a is the value, b is the name/text the user has called his element,
        # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:

            a = child.find("value").attrib.get("value")
            b = child.find("labeltext").attrib.get("text")
            c = int(child.find("list").attrib.get("list"))
            d = child.find("itemtype").attrib.get("itemtype")

            try:
                e = child.find("textvalue").attrib.get("textvalue")
                print("Number Item")
            except AttributeError:
                print("Text Item")
                e = ""

            print(
                "# Value of the " + str(d) + " item is " + str(a) + "\n" + "# Name of item is " + str(
                    b) + "\n" + "# List where it needs to be is " +
                str(c))
            logWriteNoTime("\n# Value of the " + str(d) + " item is " + str(a) + "\n" +
                           "# Name of item is " + str(b) + "\n" +
                           "# List where it needs to be is " + str(c) + "\n")

            if d == "text":
                createTextItem(self, b, a, int(c))
                createTextFile(b, basefilepath, a)
            elif d == "number":
                createNumberItem(self, b, a, int(c), e)
                createTextFile(b, basefilepath, str(e + a))
            else:
                information("The Element could not be loaded! The data may have been corrupted!")
                logWrite("The Element could not be loaded! The data may have been corrupted!")
    except xml.etree.ElementTree.ParseError:
        print("No Files found")
        logWrite("No Files found")
    except AttributeError:
        print("File not readable!")
        logWrite("Autosave not readable!")
    except FileNotFoundError:
        print("No file selected")
    logWriteNoTime("\n")


def setFilePath(self, oldpath):
    # Transition and check interaction function to change the custom filepath parameter
    text, ok = QInputDialog.getText(self, 'Enter Path',
                                    'Enter the desired path for your objects. \nWarning! All Changes since the last '
                                    'Update will be lost!\n \n' +
                                    "Textfiles are at path: " + oldpath)
    logWrite("Filepath change detected. New file path should be " + str(text))
    if len(text) > 0:
        if ":" in text:
            # delete the old textfiles folder so theres no garbage floating around
            emptyDir(oldpath + savestate.symbol + "textfiles")

            setNewFilePath(self, text)

        else:
            information("Make sure the path you enter is valid!")
            logWrite("No valid path entered, exiting...")
    else:
        logWrite("No path entered - nothings changed!")


def setNewFilePath(self, path):
    # initialize the file path and create the standard files at that location
    print(path)
    logWrite("New textfilepath will be " + str(path))
    createStandardFiles(path, 1)

    logWrite("Created the new textfiles at new path")
    # set the new filepath into the xml document so it gets saved for the next startup
    tree = ET.parse(standardFilePath + savestate.symbol + "config.xml")
    root = tree.getroot()

    root[0][0].set("path", path)
    tree.write(standardFilePath + savestate.symbol + "config.xml")
    print(root[0][0].attrib)

    # reset the two list widgets and reload the items from the xml
    self.ui.listWidget.clear()
    self.ui.listWidget_2.clear()

    createListFiles(self, path)
