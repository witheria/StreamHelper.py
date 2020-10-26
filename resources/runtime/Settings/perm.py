from resources.runtime.functions import information
from resources.runtime.Settings.logfunctions import logWriteNoTime, logWrite
from resources.runtime.textlists.program import addToList

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def getSave(self, child):
    # After parsing we need to get the values for each field. Then we put it in the list. Sorry for the naming here.
    # a is the value, b is the name/text the user has called his element,
    # c is the list in which it should be; 0 means left 1 means right
    # e defines the "pretext" item used in the number widget line edit field

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
        itemid = 0
        addToList(self, b, itemid, str(a), int(c), pretext="")
    elif d == "number":
        itemid = 1
        addToList(self, b, itemid, a, int(c), e)
    else:
        information("The Element could not be loaded! The data may have been corrupted!")
        logWrite("The Element could not be loaded! The data may have been corrupted!")

    result = {
        1: a,
        2: b,
        3: c,
        4: d,
        5: e
    }
    return result
