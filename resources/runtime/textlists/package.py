import sys

from PyQt5.QtGui import QIcon
from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.eSports import package
from resources.runtime.functions import erroreasy, information, confirmation, itemSelect
from resources.runtime.textfiles.fileedit import initTextFiles
from resources.runtime.textlists.program import addToList, getTextOfItem, updateLists


# basic loading and startup operations


def txlinit(self):
    """
    Used to initialize the basic UI.

    :type self: Settings
    :return uic type
    """
    window = None
    try:
        logWrite("Initializing the basic ui...")
        self.ui = uic.loadUi(savestate.SOURCE_PATH + 'uis' + savestate.symbol + 'main030.ui')
        window = self.ui
        self.ui.show()
        # Save the listwidgets to savestate for unbound use
        savestate.saveLists["Left"] = self.ui.listWidget
        savestate.saveLists["Right"] = self.ui.listWidget_2

        self.ui.listWidget.setToolTip(savestate.configList["LeftListName"])
        self.ui.listWidget_2.setToolTip(savestate.configList["RightListName"])

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

    # Set bindings to the ui buttons
    window.addleft.setChecked(True)
    window.addButton.clicked.connect(lambda: addListElement(self))
    window.updateButton.clicked.connect(lambda: getTextOfItem())
    window.swapButton.clicked.connect(lambda: swapLists())
    window.resetButton.clicked.connect(lambda: resetLists())
    window.allDeleteButton.clicked.connect(lambda: deleteAllItems())
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
            if key in text or text[len(text) - 1] == " " or text[len(text) - 1] == ".":
                information("This name can not be used!")
                addListElement(self)
                return None
    except IndexError:
        pass
    if len(text) > 24:
        information("The name is too long!")
        addListElement(self)
        return None

    # process the input data
    slist = 0
    if self.ui.addright.isChecked():
        slist = 1
    value = ""

    if ok:
        logWrite("Adding an element with name " + text + " to list " + str(slist))
        addToList(text, item, value, slist, pretext="")


def swapLists():
    """
    This method swaps the items in the two lists

    :return: None
    """
    logWrite("Swapping the items in the two lists...")
    temp = savestate.saveListData["Left"]
    savestate.saveListData["Left"] = savestate.saveListData["Right"]
    savestate.saveListData["Right"] = temp
    # print(temp, savestate.saveListData)
    updateLists()
    initTextFiles("initFolders")


def resetLists():
    """
    This method resets the value of every item

    :return: None
    """
    logWrite("Resetting the value of every item...")
    listl = savestate.saveListData["Left"]
    listr = savestate.saveListData["Right"]
    for key in listl:
        listl[key]["itemData"]["value"] = ""
        if "pretext" in listl[key]["itemData"]:
            listl[key]["itemData"]["pretext"] = ""
    for key in listr:
        listr[key]["itemData"]["value"] = ""
        if "pretext" in listr[key]["itemData"]:
            listr[key]["itemData"]["pretext"] = ""
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
