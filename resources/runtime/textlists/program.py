import pyperclip
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QListWidgetItem
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.functions import information
from resources.runtime.textfiles.fileedit import getTextOfItem


def addToList(text: str, itemid: int, value: str, slist: int, pretext: str):
    """
    Creates an item for further usage, saves the item and displays it in the list
    :param pretext: str
    :type text: str
    :type itemid: int
    :type value: str
    :type slist: int
    """
    endlist = savestate.saveLists["Left"]
    suplist = "Left"
    if slist == 1:
        endlist = savestate.saveLists["Right"]
        suplist = "Right"
    elif slist > 1:
        print("There is no list assigned to that number!")

    if itemid == 0:
        args = {"name": text, "value": value}
        item = TextItem(endlist, args)
        try:
            savestate.saveListItems[suplist][endlist.count() - 1] = {"item": item}
            savestate.saveListData[suplist][endlist.count() - 1] = {"itemData": item.getProperties()}
        except KeyError:
            pass

        # print("Saved: ", savestate.saveListData)
        # print("Items look like this: ", savestate.saveListItems)

    if itemid == 1:
        args = {"name": text, "value": value, "pretext": pretext}
        item = NumberItem(endlist, args)

        savestate.saveListItems[suplist][endlist.count() - 1] = {"item": item}
        savestate.saveListData[suplist][endlist.count() - 1] = {"itemData": item.getProperties()}

        # print("Saved: ", savestate.saveListData)
        # print("Items look like this: ", savestate.saveListItems)
    if itemid == 2:
        pass  # TODO: ChronoItem implementation
    elif itemid > 2:
        print("There is no item assigned to this index!")
        information("This item is not implemented in this version!")


def deleteFromItem(name):
    lkey = 0
    rkey = 0
    newlistright = {}
    newlistleft = {}
    print("Trying to delete: ", name)
    logWrite("Trying to delete: " + name)
    for item in savestate.saveListData["Left"]:
        if savestate.saveListData["Left"][item]["itemData"]["name"] != name:
            newlistleft[lkey] = savestate.saveListData["Left"][item]
            savestate.saveListItems["Left"][lkey] = savestate.saveListItems["Left"][item]
            lkey += 1
        else:
            pass
    for item in savestate.saveListData["Right"]:
        if savestate.saveListData["Right"][item]["itemData"]["name"] != name:
            newlistright[rkey] = savestate.saveListData["Right"][item]
            savestate.saveListItems["Right"][rkey] = savestate.saveListItems["Right"][item]
            rkey += 1
    savestate.saveListData.pop("Left", None)
    savestate.saveListData.pop("Right", None)
    savestate.saveListData["Left"] = newlistleft
    savestate.saveListData["Right"] = newlistright

    # print(savestate.saveListData)
    updateLists()


def updateLists():
    """
    reset all the items and lists so we can load it from the data
    :return None
    """
    logWrite("Updating the lists...")
    try:
        savestate.saveLists["Left"].clear()
        savestate.saveLists["Right"].clear()
    except AttributeError:
        # If there are for some reason no lists saved
        print("List error - There are no lists!")
    savestate.saveListItems = {"Left": {}, "Right": {}}

    # perform a miracle and resurrect all items from savestate
    for key in savestate.saveListData["Left"]:
        if "pretext" in savestate.saveListData["Left"][key]["itemData"]:
            addToList(savestate.saveListData["Left"][key]["itemData"]["name"],
                      1,
                      savestate.saveListData["Left"][key]["itemData"]["value"],
                      0,
                      savestate.saveListData["Left"][key]["itemData"]["pretext"]
                      )
        else:
            addToList(savestate.saveListData["Left"][key]["itemData"]["name"],
                      0,
                      savestate.saveListData["Left"][key]["itemData"]["value"],
                      0,
                      pretext=""
                      )

    # List 2
    for key in savestate.saveListData["Right"]:
        savestate.saveListData["Right"][int(key)] = savestate.saveListData["Right"][key]

        if "pretext" in savestate.saveListData["Right"][key]["itemData"]:
            addToList(savestate.saveListData["Right"][key]["itemData"]["name"],
                      1,
                      savestate.saveListData["Right"][key]["itemData"]["value"],
                      1,
                      savestate.saveListData["Right"][key]["itemData"]["pretext"]
                      )
        else:
            addToList(savestate.saveListData["Right"][key]["itemData"]["name"],
                      0,
                      savestate.saveListData["Right"][key]["itemData"]["value"],
                      1,
                      pretext=""
                      )
    # Update the textfiles
    getTextOfItem()


class TextItem:
    parent = QListWidgetItem
    name = ""
    value = ""
    onEdit = savestate.configList["AutoUpdateFiles"]

    def __init__(self, listwidget, *args):
        super().__init__()

        # print(args)

        self.name = args[0]["name"]
        self.value = args[0]["value"]
        self.path = savestate.configList["CustomFilePath"] + "/textfiles/Lists/"

        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "TextFileWidget.ui")

        self.setName(self.name)
        self.setValue(self.value)

        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setSizeHint(QSize(270, 80))
        listwidget.addItem(item)

        listwidget.setItemWidget(item, self.ui)
        self.parent = listwidget

        self.ui.deleteFromItem.clicked.connect(lambda: deleteFromItem(self.name))
        self.ui.lineEdit.editingFinished.connect(lambda: self.updateSelf())
        self.ui.copyPath.clicked.connect(lambda: self.getPath())

    def getValue(self):
        return self.ui.lineEdit.text()

    def getName(self):
        return self.ui.label.text()

    def getList(self):
        return self.parent

    def setValue(self, value: str):
        self.ui.lineEdit.setText(value)

    def setName(self, name: str):
        self.ui.label.setText(name)

    def setList(self, slist: QListWidgetItem):
        self.parent = slist

    def updateSelf(self):
        if self.onEdit:
            self.name = self.getName()
            self.value = self.getValue()
            getTextOfItem()

    def getProperties(self):
        arr = {"name": self.getName(), "value": self.getValue()}
        return arr

    def setEdit(self, autoedit):
        self.onEdit = autoedit

    def getPath(self):

        copy: str = ""

        if savestate.configList["ListSplit"]:
            if self.parent is savestate.saveLists["Left"]:
                copy = str(self.path + savestate.configList["LeftListName"] +
                           savestate.symbol + self.ui.label.text() + ".txt")
            elif self.parent is savestate.saveLists["Right"]:
                copy = str(self.path + savestate.configList["RightListName"] +
                           savestate.symbol + self.ui.label.text() + ".txt")
            else:
                information("This item has no file!")
        else:
            copy = str(self.path + self.ui.label.text() + ".txt")
        try:
            if savestate.symbol == "\\":
                pyperclip.copy(copy.replace("/", "\\"))
            else:
                pyperclip.copy(copy)
        except FileNotFoundError:
            print("This exception should not exist, so it has no proper handling")


class NumberItem:
    parent = QListWidgetItem
    name = ""
    value = 0
    pretext = ""
    onEdit = savestate.configList["AutoUpdateFiles"]

    def __init__(self, listwidget, *args):
        super().__init__()

        self.name = args[0]["name"]
        try:
            self.value = int(args[0]["value"])
        except ValueError:
            print("No value given for number, proceeding with standard...")

        self.pretext = args[0]["pretext"]

        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "NumberWidget.ui")

        self.setName(self.name)
        self.setValue(self.value)
        self.setPretext(self.pretext)
        self.path = savestate.configList["CustomFilePath"] + "/textfiles/Lists/"

        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setSizeHint(QSize(270, 80))
        listwidget.addItem(item)

        listwidget.setItemWidget(item, self.ui)
        self.parent = listwidget

        self.ui.deleteFromItem.clicked.connect(lambda: deleteFromItem(self.name))
        self.ui.lineEdit.editingFinished.connect(lambda: self.updateSelf())
        self.ui.spinBox.valueChanged.connect(lambda: self.updateSelf())
        self.ui.copyPath.clicked.connect(lambda: self.getPath())

    def getValue(self):
        return self.ui.spinBox.value()

    def getName(self):
        return self.ui.label.text()

    def getPretext(self):
        return self.ui.lineEdit.text()

    def getList(self):
        return self.parent

    def setValue(self, value: int):
        self.ui.spinBox.setValue(value)

    def setName(self, name: str):
        self.ui.label.setText(name)

    def setPretext(self, pretext: str):
        self.ui.lineEdit.setText(pretext)

    def setList(self, slist: QListWidgetItem):
        self.parent = slist

    def updateSelf(self):
        if self.onEdit:
            self.name = self.getName()
            self.value = self.getValue()
            self.pretext = self.getPretext()
            getTextOfItem()

    def getProperties(self):
        arr = {"name": self.getName(), "value": self.getValue(), "pretext": self.getPretext()}
        return arr

    def setEdit(self, autoedit):
        self.onEdit = autoedit

    def getPath(self):

        copy: str = ""

        if savestate.configList["ListSplit"]:
            if self.parent is savestate.saveLists["Left"]:
                copy = str(self.path + savestate.configList["LeftListName"] +
                           savestate.symbol + self.ui.label.text() + ".txt")
            elif self.parent is savestate.saveLists["Right"]:
                copy = str(self.path + savestate.configList["RightListName"] +
                           savestate.symbol + self.ui.label.text() + ".txt")
            else:
                information("This item has no file!")
        else:
            copy = str(self.path + self.ui.label.text() + ".txt")
        try:
            if savestate.symbol == "\\":
                pyperclip.copy(copy.replace("/", "\\"))
            else:
                pyperclip.copy(copy)
        except FileNotFoundError:
            print("This is a test exception")
