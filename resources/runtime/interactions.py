import shutil
import xml

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog, QFileDialog
from qtpy import uic

from resources import information
from resources.runtime import savestate
from resources.runtime.functions import setNewFilePath

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def addListElement(self):
    # Add an element to one of the lists with full user interaction.

    # text, ok = QInputDialog.getText(self, 'Enter Name',
    # 'Enter the desired name for your object:')
    itemselect = uic.loadUi("SelectionDialog.ui")
    itemselect.setWindowTitle("Itemselection")
    itemselect.exec_()
    item = itemselect.select.currentIndex()
    text = itemselect.name.text()
    ok = itemselect.buttonBox.accepted
    if item == 1:
        # Creates a NUMBER
        if ok:
            createNumberItem(self, text)
            savestate.itemorder.append(savestate.itemType.NUMBER)
    elif item == 0:
        # Creates a TEXT Item
        if ok:
            createTextItem(self, text)
            savestate.itemorder.append(savestate.itemType.TEXT)
    elif item == 2:
        # Creates a CERTAINTEXT Item which allows the user to input a number of texts and change them at will
        if ok:
            information("Not implemented yet!")
            # savestate.itemorder.append(savestate.itemType.CERTAINTEXT) TODO
    elif item == 3:
        # Creates a CHRONOS item which writes time or dates to textfiles
        if ok:
            information("Not implemented yet!")
            # savestate.itemorder.append(savestate.itemType.CHRONOS) TODO


def createTextItem(self, text, *value, **list):
    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2
    if self.ui.addright.isChecked() or list == 1:

        savestate.count = rightOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))

        wid = uic.loadUi("TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        if value:
            wid.lineEdit.setText(value)
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, savestate.count + 1)
        item[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(item[savestate.count])
        rightOne.setItemWidget(item[savestate.count], wid)

    elif self.ui.addleft.isChecked() or list == 0:
        savestate.count = leftOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        wid = uic.loadUi("TextFileWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)
        if value:
            wid.lineEdit.setText(value)
        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, text)
        item[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(item[savestate.count])
        leftOne.setItemWidget(item[savestate.count], wid)

    else:
        information("Please select a list to add the object!")


def createNumberItem(self, text, *value, **list):
    leftOne = self.ui.listWidget
    rightOne = self.ui.listWidget_2
    if self.ui.addright.isChecked() or list == 1:

        savestate.count = rightOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))

        wid = uic.loadUi("NumberWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        if value:
            wid.spinbox.setValue(value)

        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, savestate.count + 1)
        item[savestate.count].setSizeHint(QSize(270, 80))
        rightOne.addItem(item[savestate.count])
        rightOne.setItemWidget(item[savestate.count], wid)

    elif self.ui.addleft.isChecked() or list == 0:
        savestate.count = leftOne.count()
        item = {savestate.count: str(text)}
        print("Added item: " + str(item))
        wid = uic.loadUi("NumberWidget.ui")
        wid.setStyleSheet(savestate.shortBorder)
        wid.label.setText(text)

        if value:
            wid.spinbox.setValue(value)

        item[savestate.count] = QListWidgetItem()
        item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
        item[savestate.count].setData(5, text)
        item[savestate.count].setSizeHint(QSize(270, 80))
        leftOne.addItem(item[savestate.count])
        leftOne.setItemWidget(item[savestate.count], wid)

    else:
        information("Please select a list to add the object!")


def setFilePath(self):
    # Transition and check interaction function to change the custom filepath parameter
    text, ok = QInputDialog.getText(self, 'Enter Path',
                                    'Enter the desired path for your objects:')
    if len(text) > 0:
        if ":" in text:
            setNewFilePath(text)
        else:
            information("Make sure the path you enter is valid!")
    else:
        information("Make sure the path you enter is valid!")


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
        wid = uic.loadUi("TextFileWidget.ui")
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
        wid = uic.loadUi("TextFileWidget.ui")
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


def autListElement(self, name, nr, value, itemType):
    if itemType == 0:
        createTextItem(self, name, value, nr)
    elif itemType == 1:
        createNumberItem(self, name, value, nr)
    else:
        print("Not a valid Item!")


def getTextOfItem(self, path, *item):
    # This function gets the text from within the List Widgets, first from the left list, then from the other one it
    # will also write these texts into the xml and text files. If there is an item given it will internally return
    # that item in the form: "text" #unique "label" so it can be split. item should be a number

    # init the xml file for the textfiles
    xmlFile = open(path + "\\autosave.xml", "w+")

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

        if itemtype == "number":
            # Set the list in which the item lays for revive purposes
            listnr = ET.SubElement(itemdirect[index], "list")
            listnr.set("list", "0")
            # Now the values of the item
            value1int = str(self.ui.listWidget.itemWidget(current).spinBox.value())
            value2int = str(self.ui.listWidget.itemWidget(current).spinBox_2.value())
            value3int = str(self.ui.listWidget.itemWidget(current).spinBox_3.value())

            value1 = ET.SubElement(itemdirect[index], "value")
            value1.set("value1", value1int)
            value2 = ET.SubElement(itemdirect[index], "value")
            value2.set("value2", value2int)
            value3 = ET.SubElement(itemdirect[index], "value")
            value3.set("value3", value3int)
            # And now the label
            labeltext = ET.SubElement(itemdirect[index], "labeltext")
            labeltext.set("text", label)

        # Out to the log it goes
        print("text of item", itemdirect[index], "saved to file")

        # List 2

    for index in range(0, self.ui.listWidget_2.count()):
        # Get the current element on index
        current = self.ui.listWidget_2.item(index)

        # Save the two fields that are customizable
        text = self.ui.listWidget_2.itemWidget(current).lineEdit.text()
        label = self.ui.listWidget_2.itemWidget(current).label.text()
        # Create the XML Tree element
        itemdirect[index] = ET.SubElement(data, ("item" + str(index)))

        # Save the type of the item
        Listtype = ET.SubElement(itemdirect[index], "itemtype")
        Listtype.set("itemtype", str(self.ui.listWidget_2.itemWidget(current).whatsThis()))

        # Set the list in which the item lays for revive purposes
        listnr = ET.SubElement(itemdirect[index], "list")
        listnr.set("list", "1")
        # Now the value of the item
        value1 = ET.SubElement(itemdirect[index], "value")
        value1.set("value", text)
        # And now the label
        labeltext = ET.SubElement(itemdirect[index], "labeltext")
        labeltext.set("text", label)

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


def createListFiles(self, path):
    print("Trying to recall what was in the list... \n")
    # Lets look in the xml so we know what was up
    try:
        source = ET.parse(path + "\\autosave.xml")
        sourceroot = source.getroot()

    # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here,
    # its really quite obvious though. a is the value, b is the name/text the user has called his element,
    # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:

            a = child.find("value").attrib.get("value")
            b = child.find("labeltext").attrib.get("text")
            c = int(child.find("list").attrib.get("list"))
            # d = child.find("itemtype").attrib.get("type")

            # x = next(iter(a.values()))

            print(
                "# Value of item is " + a + "\n" + "# Name of item is " + b + "\n" + "# List where it needs to be is " +
                str(c))
            if c == 1:
                autTextListElement(self, b, 1, a)
            elif c == 0:
                autTextListElement(self, b, 0, a)
            else:
                information("The Element could not be loaded! The data may have been corrupted!")
    except xml.etree.ElementTree.ParseError:
        print("No Files found")
    except AttributeError:
        print("Not readable!")


def saveConfig(self, basefilepath):
    # saves the current lists to a separate file
    filepath = QFileDialog.getSaveFileName(self, "Create Save", basefilepath, ".oi")
    file = str(filepath[0] + ".oi")
    savefile = shutil.copy(str(savestate.standardFilePath +"\\autosave.xml"), file)


def loadConfig(self, basefilepath):
    # Loads a save file
    file = QFileDialog.getOpenFileName(self, "Open Save", basefilepath, "*.oi")
    self.ui.listWidget.clear()
    self.ui.listWidget_2.clear()
    print(str(file))
    try:
        source = ET.parse(file[0])
        sourceroot = source.getroot()

        # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here,
        # its really quite obvious though. a is the value, b is the name/text the user has called his element,
        # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:

            a = child.find("value").attrib.get("value")
            b = child.find("labeltext").attrib.get("text")
            c = int(child.find("list").attrib.get("list"))
            # d = child.find("itemtype").attrib.get("type")

            # x = next(iter(a.values()))

            print(
                "# Value of item is " + a + "\n" + "# Name of item is " + b + "\n" + "# List where it needs to be is " +
                str(c))
            if c == 1:
                autTextListElement(self, b, 1, a)
            elif c == 0:
                autTextListElement(self, b, 0, a)
            else:
                information("The Element could not be loaded! The data may have been corrupted!")
    except xml.etree.ElementTree.ParseError:
        print("File not readable!")