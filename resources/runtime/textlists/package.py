import sys

from PyQt5.QtGui import QIcon
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.eSports import package
from resources.runtime.functions import erroreasy, information, confirmation, itemSelect
from resources.runtime.textfiles.fileedit import initTextFiles
from resources.runtime.textlists.program import addToList, getTextOfItem, updateLists, resetAccessesToChrono


def txlinit(self):
    """
    Used to initialize the basic UI.

    :type self: StreamHelper
    :return uic type
    """
    try:
        logWrite("Initializing the basic ui...")
        print(f"Checking for main ui file here: {savestate.SOURCE_PATH + 'uis' + savestate.symbol + 'main031.ui'}")
        self.ui = uic.loadUi(savestate.SOURCE_PATH + 'uis' + savestate.symbol + 'main031.ui')
        window = self.ui
        window.tabWidget.setCurrentIndex(savestate.configList["StartupTab"])
        self.ui.show()

        # Save the listwidgets to savestate for unbound use
        savestate.saveLists["Left"] = self.ui.listWidget
        savestate.saveLists["Right"] = self.ui.listWidget_2

        self.ui.listWidget.setToolTip(savestate.configList["LeftListName"])
        self.ui.listWidget_2.setToolTip(savestate.configList["RightListName"])

        # self.ui.listWidget.setDragDropMode(QAbstractItemView.DragDrop)
        # self.ui.listWidget_2.setDragDropMode(QAbstractItemView.DragDrop)

    except FileNotFoundError:
        erroreasy("The main user interface could not be loaded. Try reinstalling the program. "
                  "Please notify the developer if this error persists", 0x0001)
        logWrite("The main user interface could not be loaded. Try reinstalling the program. "
                 "Please notify the developer if this error persists")
        sys.exit(0)

    # Get the List back up from the json and revisit the TXTs so they are what they were on last startup
    # createListFiles()

    # init the eSports ui part
    package.initPackage(self.ui)

    # Add icons to the buttons
    window.addButton.setIcon(QIcon(":/images/common/add.png"))
    window.updateButton.setIcon(QIcon(":/images/common/update.png"))
    window.swapButton.setIcon(QIcon(":/images/common/swap.png"))
    window.resetButton.setIcon(QIcon(":/images/common/reset.png"))
    window.allDeleteButton.setIcon(QIcon(":/images/common/delete.png"))
    window.toLeft.setIcon(QIcon(savestate.SOURCE_PATH + "/images/common/toLeft.png"))
    window.toRight.setIcon(QIcon(savestate.SOURCE_PATH + "/images/common/toRight.png"))

    # Set bindings to the ui buttons
    window.addleft.setChecked(True)
    window.addButton.clicked.connect(lambda: addListElement(self))
    window.updateButton.clicked.connect(lambda: getTextOfItem())
    window.swapButton.clicked.connect(lambda: swapLists(window))
    window.resetButton.clicked.connect(lambda: resetLists())
    window.allDeleteButton.clicked.connect(lambda: deleteAllItems())
    window.toLeft.clicked.connect(lambda: moveSelected(0))
    window.toRight.clicked.connect(lambda: moveSelected(1))

    # make sure the access counter gets set to zero every second
    savestate.timer.timeout.connect(lambda: resetAccessesToChrono())
    return window


def addListElement(self):
    """
    Add an element to one of the lists with full user interaction.

    :type self: StreamHelper

    :return: None
    """
    # create a user dialog from which we get the name and the type of the item to be created
    itemselect = itemSelect()
    ok, item, text = itemselect.exec()
    try:
        for key in savestate.forbiddenChars:
            if key in text or text[-1] == " " or text[-1] == ".":
                information("This name can not be used!")
                addListElement(self)
                return
    except IndexError:
        pass
    if len(text) > 24:
        information("The name is too long!")
        addListElement(self)
        return

    if text in savestate.saveListItemNames:
        information("This name already exists. Please make sure the names\nyou pick are unique")
        addListElement(self)
        return

    # process the input data
    slist = 0
    if self.ui.addright.isChecked():
        slist = 1
    if item == 2:
        value = "00:00:00"
    else:
        value = ""

    if ok:
        logWrite("Adding an element with name " + text + " to list " + str(slist))
        addToList(text.strip(), item, value, slist, pretext="")
        return


def swapLists(window):
    """
    This method swaps the items in the two lists

    :return: None
    """
    if window.onlySelectedActivated.isChecked():
        moveSelected(2)
        return
    logWrite("Swapping the items in the two lists...")
    temp = savestate.saveListData["Left"]
    savestate.saveListData["Left"] = savestate.saveListData["Right"]
    savestate.saveListData["Right"] = temp
    print(temp, savestate.saveListData)
    updateLists()
    initTextFiles("initFolders")


def resetLists():
    """
    This method resets the value of every item

    :return: None
    """
    logWrite("Resetting the value of every item...")
    for key1 in savestate.saveListData:
        for key2 in savestate.saveListData[key1]:
            savestate.saveListData[key1][key2]["itemData"]["value"] = ""
            if "pretext" in savestate.saveListData[key1][key2]["itemData"]:
                savestate.saveListData[key1][key2]["itemData"]["pretext"] = ""
            if "chronotype" in savestate.saveListData[key1][key2]["itemData"]:
                savestate.saveListData[key1][key2]["itemData"]["valueTime"] = "0:0:0"
                savestate.saveListData[key1][key2]["itemData"]["running"] = False
            if "path" in savestate.saveListData[key1][key2]["itemData"]:
                savestate.saveListData[key1][key2]["itemData"]["path"] = ""
    updateLists()


def deleteAllItems():
    """
    This method deletes every item in the lists

    :return: None
    """
    if confirmation("Delete all items and textfiles?"):
        logWrite("Deleting all items from the lists...")
        savestate.saveListData = {"Left": {}, "Right": {}}
        updateLists()
        initTextFiles("initFolders")


def moveSelected(direction: int) -> None:
    """
    This method swaps or moves selected items.
        direction == 0: move to the left list
        direction == 1: move to the right list
        direction == 2: swap both lists (selected)

    :return: None
    """
    if direction == 0:
        # go through the list we are taking from and find all selected items
        temp: dict = {}
        newRight: dict = {}
        for key2 in savestate.saveListData["Right"]:
            if savestate.saveListItems["Right"][key2]["item"].getSelected():
                temp[key2] = savestate.saveListData["Right"][key2]
            else:
                newRight[key2] = savestate.saveListData["Right"][key2]
        # merge the two new dicts we got into one new dict and this will be the new left one
        savestate.saveListData["Left"] = mergeDicts(savestate.saveListData["Left"], temp)
        # we will have to renumerate the old right one (since we took some items from inbetween)
        savestate.saveListData["Right"] = \
            {item: list(newRight.values())[item] for item in range(0, len(list(newRight.values())))}
        updateLists()
        initTextFiles("initFolders")

    if direction == 1:
        # go through the list we are taking from and find all selected items
        temp: dict = {}
        newRight: dict = {}
        for key2 in savestate.saveListData["Left"]:
            if savestate.saveListItems["Left"][key2]["item"].getSelected():
                temp[key2] = savestate.saveListData["Left"][key2]
            else:
                newRight[key2] = savestate.saveListData["Left"][key2]
        # merge the two new dicts we got into one new dict and this will be the new left one
        savestate.saveListData["Right"] = mergeDicts(savestate.saveListData["Right"], temp)
        # we will have to renumerate the old right one (since we took some items from inbetween)
        savestate.saveListData["Left"] = \
            {item: list(newRight.values())[item] for item in range(0, len(list(newRight.values())))}
        updateLists()
        initTextFiles("initFolders")

    elif direction == 2:
        logWrite("Swapping every selected item")
        temp: dict = {"Left": {}, "Right": {}}
        for key1 in savestate.saveListData:
            for key2 in savestate.saveListData[key1]:
                if savestate.saveListItems[key1][key2]["item"].getSelected():
                    temp[key1][key2] = savestate.saveListData[key1][key2]


def mergeDicts(onedict, twodict) -> dict:
    """
    A function to merge sorted dicts into one another (used for the moveSelected() function)

    only works if the keys are numbers and sorted

    :type onedict: dict
    :type twodict: dict
    :return: dict
    """
    result: dict = {}
    newthing = list(onedict.values())

    for key in twodict:
        newthing.insert(key, twodict[key])
    for item in range(0, len(newthing)):
        result[item] = newthing[item]

    # result = {item: newthing[item] for item in range(0, len(newthing))}
    return result
