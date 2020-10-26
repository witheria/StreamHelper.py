from qtpy import uic

from resources.runtime import savestate
from resources.runtime.Settings.perm import getSave
from resources.runtime.functions import erroreasy
from resources.runtime.textfiles.fileedit import createListFiles
from resources.runtime.textlists.program import addToList, getTextOfItem

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# basic loading and startup operations


def txlinit(self, newfilepath, oldfilepath):
    """
    :type self: StreamHelper
    :type newfilepath: String
    :type oldfilepath: String
    """
    try:
        self.ui = uic.loadUi('uis' + savestate.symbol + 'main.ui')
        window = self.ui
        self.ui.show()

    except FileNotFoundError:
        erroreasy("The main user interface could not be loaded. Try reinstalling the program. "
                  "Please notify the developer if this error persists", 0x0001)
    # Set bindings to the ui buttons

    # Get the List back up from the xml and revisit the TXTs so they are what they were on last startup
    createListFiles(self, oldfilepath)

    window.addButton.clicked.connect(lambda: addListElement(self))
    window.updateButton.clicked.connect(lambda: getTextOfItem(self, oldfilepath, newfilepath))

    return window


def addListElement(self):
    # Add an element to one of the lists with full user interaction.

    # create a user dialog from which we get the name and the type of the item to be created
    itemselect = uic.loadUi("uis" + savestate.symbol + "SelectionDialog.ui")
    itemselect.setWindowTitle("Item Selection")
    itemselect.buttonBox.accepted.connect(itemselect.accept)
    itemselect.buttonBox.rejected.connect(itemselect.reject)
    ok = itemselect.exec_()
    item = itemselect.select.currentIndex()
    text = itemselect.name.text()

    print(ok)

    # process the input data

    addToList(self, text, item, value=0, slist=0, pretext="")

