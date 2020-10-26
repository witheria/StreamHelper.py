import os
import xml

from resources.runtime import savestate
from resources.runtime.Settings.perm import getSave
from resources.runtime.functions import erroreasy
from resources.runtime.Settings.logfunctions import logWrite, logWriteNoTime
from resources.runtime.textfiles.folderedit import emptyDir

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def deleteTextFile(name, path):
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")
    os.remove(filename)


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
        source = ET.parse(savestate.standardFilePath + savestate.symbol + "autosave.xml")
        sourceroot = source.getroot()
        logWrite("Parsing autosave...")

        # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here.
        # a is the value, b is the name/text the user has called his element,
        # c is the list in which it should be; 0 means left 1 means right
        for child in sourceroot:
            result = getSave(self, child)

            print(result)

            if result[4] == "text":
                createTextFile(result[2], newpath, result[1])
            elif result[4] == "number":
                createTextFile(result[2], newpath, str(result[5] + result[1]))

    except xml.etree.ElementTree.ParseError:
        print("No Files found")
        logWrite("No Files found")
    except AttributeError:
        print("File not readable!")
        logWrite("Autosave not readable!")
        erroreasy(self, "There was an error reading the old savefile! Please try to recover it or resort to a backup",
                  0x0103)

    logWriteNoTime("\n")


def createTextFile(name, path, text):
    # This method is used to create and edit the textfiles used around the program.
    filename = str(path + savestate.symbol + "textfiles" + savestate.symbol + name + ".txt")

    file = open(filename, "w+")
    file.write(text)

    file.close()
