import pyperclip
from PyQt5.QtCore import QSize, Qt, QTime
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.functions import information
from resources.runtime.textfiles.fileedit import getTextOfItem, copyImage


def addToList(text: str, itemid: int, value: str, slist: int, pretext: str):
    """
    Creates an item for further usage, saves the item and displays it in the list

    :type pretext: str
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
        # Add a text item
        if not savestate.configList["AllowedItems"]["Text Item"]:
            return
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
        # Add a number item
        if not savestate.configList["AllowedItems"]["Number Item"]:
            return
        args = {"name": text, "value": value, "pretext": pretext}
        item = NumberItem(endlist, args)

        try:
            savestate.saveListItems[suplist][endlist.count() - 1] = {"item": item}
            savestate.saveListData[suplist][endlist.count() - 1] = {"itemData": item.getProperties()}
        except KeyError:
            pass

        # print("Saved: ", savestate.saveListData)
        # print("Items look like this: ", savestate.saveListItems)
    if itemid == 2:
        if not savestate.configList["AllowedItems"]["Chrono Item"]:
            return
        # Add a chrono item. Chronotype will be ignored if given in valueTime
        args = {"name": text, "valueTime": value, "chronotype": 0, "returnMsg": pretext}
        item = ChronoItem(endlist, args)

        try:
            savestate.saveListItems[suplist][endlist.count() - 1] = {"item": item}
            savestate.saveListData[suplist][endlist.count() - 1] = {"itemData": item.getProperties()}
        except KeyError:
            pass
    if itemid == 3:
        if not savestate.configList["AllowedItems"]["Image Item"]:
            return
        # Adds an image item to the list, containing the path to an image and a custom name
        args = {"name": text, "path": value, "optionalArgs": pretext}
        item = ImageItem(endlist, args)

        try:
            savestate.saveListItems[suplist][endlist.count() - 1] = {"item": item}
            savestate.saveListData[suplist][endlist.count() - 1] = {"itemData": item.getProperties()}
        except KeyError:
            pass
    elif itemid > 3:
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
            print(newlistleft[lkey])
            savestate.saveListItems["Left"][lkey] = savestate.saveListItems["Left"][item]
            lkey += 1
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
        elif "chronotype" in savestate.saveListData["Left"][key]["itemData"]:
            addToList(savestate.saveListData["Left"][key]["itemData"]["name"],
                      2,
                      str(savestate.saveListData["Left"][key]["itemData"]["valueTime"] + ":" +
                          str(savestate.saveListData["Left"][key]["itemData"]["running"]) + ":" +
                          str(savestate.saveListData["Left"][key]["itemData"]["chronotype"]) + ":" +
                          str(savestate.saveListData["Left"][key]["itemData"]["customFormat"])
                          ),
                      0,
                      savestate.saveListData["Left"][key]["itemData"]["returnMsg"]
                      )
        elif "path" in savestate.saveListData["Left"][key]["itemData"]:
            addToList(savestate.saveListData["Left"][key]["itemData"]["name"],
                      3,
                      savestate.saveListData["Left"][key]["itemData"]["path"],
                      0,
                      "")
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
        elif "chronotype" in savestate.saveListData["Right"][key]["itemData"]:
            addToList(savestate.saveListData["Right"][key]["itemData"]["name"],
                      2,
                      str(savestate.saveListData["Right"][key]["itemData"]["valueTime"] + ":" +
                          str(savestate.saveListData["Right"][key]["itemData"]["running"]) + ":" +
                          str(savestate.saveListData["Right"][key]["itemData"]["chronotype"]) + ":" +
                          str(savestate.saveListData["Right"][key]["itemData"]["customFormat"])),
                      1,
                      savestate.saveListData["Right"][key]["itemData"]["returnMsg"]
                      )
        elif "path" in savestate.saveListData["Right"][key]["itemData"]:
            addToList(savestate.saveListData["Right"][key]["itemData"]["name"],
                      3,
                      savestate.saveListData["Right"][key]["itemData"]["path"],
                      1,
                      "")
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


class ChronoItem(QWidget):
    """
    Creates a QListWidgetItem to insert into the given listwidget, has getters and setters for the most important
    attributes

    Expected args: {"name": str, "valueTime": str, "chronotype": int, "returnMsg": str}

    :type parent: QListWidgetItem
    :type onEdit: bool
    :type valueHr: int
    :type valueMn: int
    :type valueSc: int
    :type chronotype: int
    :type running: bool
    :type count: int
    :type format: str
    """
    parent: QListWidget = QListWidget
    running: bool = False
    format: str = savestate.configList["ChronoFormat"]
    chronotype: int = 0
    valueHr: int = 0
    valueMn: int = 0
    valueSc: int = 0
    returnMsg: str = "This timer is done like your momma"
    name: str = ""

    def __init__(self, listwidget, *args):

        # noinspection PyArgumentList
        super().__init__()

        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "ChronoWidget.ui")

        self.format = savestate.configList["ChronoFormat"]
        timeedit: QTimeEdit = self.ui.timeEdit
        startButton: QPushButton = self.ui.startButton
        # stopButton: QPushButton = self.ui.stopButton
        resetButton: QPushButton = self.ui.resetButton
        chooseType: QComboBox = self.ui.chooseType

        self.path = savestate.configList["CustomFilePath"] + "/textfiles/Lists/"

        self.name = args[0]["name"]
        self.chronotype = args[0]["chronotype"]
        self.returnMsg = args[0]["returnMsg"]
        print(args[0]["valueTime"])
        self.valueSc = int(args[0]["valueTime"].split(":")[2])
        self.valueMn = int(args[0]["valueTime"].split(":")[1])
        self.valueHr = int(args[0]["valueTime"].split(":")[0])
        try:
            # We need some way to update the Item without resetting, so this is internal. Note: NOT EXPECTED FROM USER!
            self.running = bool((args[0]["valueTime"].split(":")[3]).replace("False", ""))

            self.chronotype = int(args[0]["valueTime"].split(":")[4].split("#F")[0])
            temp = args[0]["valueTime"].split(":")[5:]
            self.format = ":".join([x for x in temp])
            print(self.format)
        except IndexError:
            pass  # This just means that the item has been created by the user

        self.parent = listwidget
        self.updateSelf()

        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setSizeHint(QSize(270, 80))
        listwidget.addItem(item)

        listwidget.setItemWidget(item, self.ui)

        # create the file
        self.updateFileTime()

        chooseType.currentIndexChanged.connect(lambda: self.changeType())

        # chooseType.setStyleSheet("QComboBox {background:white}")

        startButton.setIcon(QIcon(savestate.SOURCE_PATH + "images/common/play_pause.png"))
        resetButton.setIcon(QIcon(savestate.SOURCE_PATH + "images/common/reset.png"))

        startButton.clicked.connect(self.startTime)
        # stopButton.pressed.connect(self.pauseTime)
        self.ui.deleteFromItem.clicked.connect(lambda: deleteFromItem(self.name))
        self.ui.copyPath.clicked.connect(lambda: self.getPath())
        self.ui.donemsg.textChanged.connect(lambda: self.setReturnMsg(self.ui.donemsg.text()))
        self.ui.format.clicked.connect(lambda: self.changeFormat())
        resetButton.pressed.connect(self.resetTimer)
        timeedit.timeChanged.connect(self.updateValues)

        savestate.timer.timeout.connect(self.differentiate)

        self.ui.show()

    def differentiate(self):
        """
        Function used to determine which kind of chronometer needs to be displayed.

        :return:
        """
        # print(f"Called {self.chronotype} {self.running}")
        if self.running:
            if self.chronotype == 1:  # Countdown
                # print("Counting down")
                self.countdown()
            if self.chronotype == 2:  # Count up
                # print("Count Up")
                self.countup()
            if self.chronotype == 3:  # show time
                self.showTime()
        self.updateFileTime()

    def countdown(self):
        if self.valueSc == 0:
            if self.valueMn == 0:
                if self.valueHr == 0:
                    self.running = False
                    self.ui.donemsg.setText(self.returnMsg)
                else:
                    self.valueMn = 59
                    self.valueHr -= 1
                    self.valueSc = 59
            else:
                self.valueSc = 59
                self.valueMn -= 1
        else:
            # print(self.valueSc)
            self.valueSc -= 1
        time: QTime = QTime(self.valueHr, self.valueMn, second=self.valueSc)
        self.ui.timeEdit.setTime(time)

    def countup(self):

        self.valueSc += 1
        if self.valueSc == 60:
            self.valueSc = 0
            self.valueMn += 1
        if self.valueMn == 60:
            self.valueMn = 0
            self.valueHr += 1
        time: QTime = QTime(self.valueHr, self.valueMn, second=self.valueSc)
        self.ui.timeEdit.setTime(time)

    def showTime(self):
        time: QTime = QTime().currentTime()
        self.ui.timeEdit.setTime(time)

    def updateValues(self):
        thistime: QTime = self.ui.timeEdit.time()
        self.valueSc = thistime.second()
        self.valueMn = thistime.minute()
        self.valueHr = thistime.hour()
        # print(thistime)

    def startTime(self):
        self.running = self.ui.startButton.isChecked()
        # self.running)
        # This shouldnt be running if its on countdown and already zero
        if self.isZero() and self.chronotype == 1:
            self.running = False

    def pauseTime(self):
        self.running = False

    def changeType(self):
        self.chronotype = self.ui.chooseType.currentIndex()

    def resetTimer(self):
        self.valueSc = 0
        self.valueMn = 0
        self.valueHr = 0
        self.running = False
        time: QTime = QTime(self.valueHr, self.valueMn, second=self.valueSc)
        self.ui.timeEdit.setTime(time)
        self.updateSelf()

    def getValue(self):
        return str(str(self.valueHr) + ":" + str(self.valueMn) + ":" + str(self.valueSc))

    def getName(self):
        return self.ui.label.text()

    def getList(self):
        return self.parent

    def getFormat(self):
        return self.format

    def isZero(self) -> bool:
        if self.valueSc == 0 and self.valueMn == 0 and self.valueHr == 0:
            return True
        else:
            return False

    def setValue(self, value: str):
        """
        value is a string in the format set by the user (standard: "hh:mm:ss")

        :param value: str
        :return: None
        """
        self.valueSc = int(value.split(":")[2])
        self.valueMn = int(value.split(":")[1])
        self.valueHr = int(value.split(":")[0])
        self.updateSelf()

    def setEdit(self, onEdit: bool):
        """Necessary function not to block getTextOfItem"""
        pass

    def setName(self, name: str):
        self.ui.label.setText(name)
        self.updateSelf()

    def setList(self, slist: QListWidget):
        self.parent = slist

    def setReturnMsg(self, text: str):
        self.returnMsg = text
        self.ui.donemsg.setText(text)
        self.updateSelf()

    def setFormat(self, newFormat: str):
        print("New format set!")
        self.format = newFormat
        self.updateSelf()

    def changeFormat(self):
        print("Format change request!")
        result, ok = QInputDialog.getText(self, "Input", "Enter a new local chrono format", QLineEdit.Normal, "")
        if ok:
            self.setFormat(result)

    def updateSelf(self):
        self.ui.label.setText(self.name)
        self.ui.chooseType.setCurrentIndex(self.chronotype)
        self.ui.donemsg.setText(self.returnMsg)
        self.ui.startButton.setChecked(self.running)
        # format = savestate.configList["ChronoFormat"]
        self.ui.timeEdit.setDisplayFormat(self.format)
        # print(self.format, self.running)

        time: QTime = QTime(self.valueHr, self.valueMn, second=self.valueSc)
        self.ui.timeEdit.setTime(time)
        self.updateFileTime()

    def getProperties(self):
        valueTime = str(str(self.valueHr) + ":" + str(self.valueMn) + ":" + str(self.valueSc))
        arr = {"name": self.name,
               "valueTime": valueTime,
               "chronotype": self.chronotype,
               "returnMsg": self.ui.donemsg.text(),
               "running": self.running,
               "customFormat": self.format
               }
        return arr

    def updateFileTime(self):
        """
        Updates the file contents associated with this item

        """
        copy = ""
        try:
            if savestate.configList["ListSplit"]:
                if self.parent is savestate.saveLists["Left"]:
                    copy = str(self.path + savestate.configList["LeftListName"] +
                               savestate.symbol + self.ui.label.text() + ".txt")
                elif self.parent is savestate.saveLists["Right"]:
                    copy = str(self.path + savestate.configList["RightListName"] +
                               savestate.symbol + self.ui.label.text() + ".txt")
                else:
                    print(self.parent, savestate.saveLists["Left"])
                    information("This item has no file!")
            else:
                copy = str(self.path + self.ui.label.text() + ".txt")
            with open(copy, "w+") as file:
                file.write(self.getTimeString())
        except FileNotFoundError:
            print("Error in " + self.name + ", the file this link points to does not exist!")
        except UnboundLocalError:
            self.updateFileTime()
        except RuntimeError:
            print("Item deleted due to runtime, rebuilding list...")

    def getTimeString(self) -> str:
        """
        Gives the currently shown time as a string

        :return: string
        """
        # print(self.isZero(), self.chronotype)
        if self.isZero() and self.chronotype == 1:
            result = self.returnMsg
        else:
            time: QTime = QTime(self.valueHr, self.valueMn, second=self.valueSc)
            result = time.toString(self.format)
        # print(result, self.format)
        return result

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
                self.updateFileTime()
        else:
            copy = str(self.path + self.ui.label.text() + ".txt")
        try:
            if savestate.symbol == "\\":
                pyperclip.copy(copy.replace("/", "\\"))
            else:
                pyperclip.copy(copy)
        except FileNotFoundError:
            print("This is a test exception")


class ImageItem:
    """
    An image item contains an image and will copy that image to the list path. With pretext handling, a custom image
    name is possible.

    This item takes 3 arguments in its constructor:
        1. The name of the image item, displayed only in the StreamHelper
        2. The path to the image, which will be copied to the list location
        #. A team, that can be assigned to an image so that operations on the team also change the image
        (PLANNED; BUT NOT YET AVAILABLE)

    :type parent: QListWidget
    :type name: str
    :type path: strq
    :type imgPath: str
    :type optionalArgsStore: str
    """
    parent = None
    name = ""
    path = ""
    # Basic filler image path, displaying the streamhelper logo. does not get displayed
    imgPath = (savestate.SOURCE_PATH + savestate.symbol + "images" + savestate.symbol + "common" + savestate.symbol +
               "icon2.png")
    optionalArgsStore = ""

    def __init__(self, listwidget, *args):
        super().__init__()

        # get the name
        self.name = args[0]["name"]
        try:
            # try to get a custom path, if there is none just leave it on default
            if args[0]["path"] != "":
                self.imgPath = args[0]["path"]
            self.optionalArgsStore = args[0]["optionalArgs"]
        except ValueError:
            print("There was no image path given! Proceeding...")

        # Load the ui
        self.ui = uic.loadUi(savestate.SOURCE_PATH + "uis" + savestate.symbol + "ImgWidget.ui")

        self.path = savestate.configList["CustomFilePath"] + "/textfiles/Lists/"

        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setSizeHint(QSize(270, 80))
        listwidget.addItem(item)

        listwidget.setItemWidget(item, self.ui)
        self.parent = listwidget

        self.setName(self.name)
        self.setValue(self.imgPath)

        self.ui.deleteFromItem.clicked.connect(lambda: deleteFromItem(self.name))
        self.ui.copyPath.clicked.connect(lambda: self.getPath())
        self.ui.loadImg.clicked.connect(lambda: self.addPicture())

    def setValue(self, value: str):
        self.ui.name.setText(value)
        self.loadPicture(value)
        self.imgPath = value
        self.copyPicture()

    def setName(self, name: str):
        self.ui.label.setText(name)

    def setList(self, slist: QListWidget):
        self.parent = slist

    def setEdit(self, value: bool):
        """
        This function is required, but since image items only update on new path load, its basically irrelevant
        """
        pass

    def getValue(self):
        return self.imgPath

    def getName(self):
        return self.ui.label.text()

    def getList(self):
        return self.parent

    def getProperties(self):
        arr = {"name": self.getName(), "path": self.getValue()}
        return arr

    def getPath(self):

        copy: str = ""

        if savestate.configList["ListSplit"]:
            if self.parent is savestate.saveLists["Left"]:
                copy = str(self.path + savestate.configList["LeftListName"] +
                           savestate.symbol + self.ui.label.text())
            elif self.parent is savestate.saveLists["Right"]:
                copy = str(self.path + savestate.configList["RightListName"] +
                           savestate.symbol + self.ui.label.text())
            else:
                information("This item has no file!")
        else:
            copy = str(self.path + self.ui.label.text())
        try:
            if savestate.symbol == "\\":
                pyperclip.copy(copy.replace("/", "\\"))
            else:
                pyperclip.copy(copy)
        except FileNotFoundError:
            print("This is a test exception")

    def loadPicture(self, path: str):
        picture = QPixmap(path)
        self.ui.picture.setScaledContents(True)

        self.ui.picture.setPixmap(picture)

    def addPicture(self):
        path, ok = QFileDialog.getOpenFileName(self.parent, "Open Image File", self.imgPath)
        if ok:
            try:
                self.setValue(path)
            except Exception as e:
                print(e)

    @staticmethod
    def getPictureType(path: str):
        """
        This method gets the image type (png, jpg, whatever)
        """
        try:
            return path.split(".")[-1]
        except Exception as e:
            print(e)

    def copyPicture(self):
        """
        This method is used to call the static method in fileedit with useful arguments
        """
        picname: str = f"{self.name}"
        plist: int = 0
        if self.parent == savestate.saveLists["Right"]:
            plist = 1
        # print("passing " + self.parent.toolTip() + " as list no")
        copyImage(self.imgPath, newName=picname, slist=plist)
