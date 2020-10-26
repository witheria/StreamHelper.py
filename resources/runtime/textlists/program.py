from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListWidgetItem
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.functions import erroreasy
from resources.runtime.Settings.logfunctions import logWrite

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# This file serves as a backend for the interface functions in package.py


def addToList(self, text: str, itemid: int, value: str, slist: int, pretext: str):
    """
    :param pretext: String
    :type self: QListWidget
    :type text: String
    :type itemid: Integer
    :type value: String
    :type slist: Integer
    """
    ilist = None
    # This Method adds the desired item-type to one of the lists selected. Was formerly split into 6 methods
    # slist, value and pretext are optional arguments, used only by certain widgets
    if slist == 0:
        ilist = self.ui.listWidget
    elif self.ui.addright.isChecked() or slist == 1:
        ilist = self.ui.listWidget_2
    elif slist > 1:
        pass

    savestate.count = ilist.count()
    item = {savestate.count: str(text)}
    print("Added item: " + str(item))
    logWrite("Added item: " + str(item[savestate.count]) + "\n")
    if itemid is 0:
        wid = uic.loadUi("uis" + savestate.symbol + "TextFileWidget.ui")
        wid.setWhatsThis("text")
        if value:
            wid.lineEdit.setText(value)
    elif itemid is 1:
        wid = uic.loadUi("uis" + savestate.symbol + "NumberWidget.ui")
        wid.setWhatsThis("number")
        wid.spinBox.setValue(int(value))
        wid.lineEdit.setText(pretext)
    elif itemid is 2:
        wid = uic.loadUi("uis" + savestate.symbol + "ChronoWidget.ui")
        wid.setWhatsThis("chrono")
    else:
        erroreasy(self, "There was an error selecting your item-type, please try again. If this error persists, "
                        "reinstall the program.", 0x0003)
        return
    wid.setStyleSheet(savestate.shortBorder)
    wid.label.setText(text)

    setItem(item, ilist, text, wid)


def setItem(item, ilist, text, wid):
    # this method adds the item to the desired list. The method outsources and generalizes the code.

    item[savestate.count] = QListWidgetItem()
    item[savestate.count].setFlags(item[savestate.count].flags() | Qt.ItemIsEditable)
    item[savestate.count].setData(5, text)
    item[savestate.count].setSizeHint(QSize(270, 80))
    ilist.addItem(item[savestate.count])
    ilist.setItemWidget(item[savestate.count], wid)


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


def createTextFile(name, path, text):
    # This method is used to create and edit the textfiles used around the program.
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")

    file = open(filename, "w+")
    file.write(text)

    file.close()