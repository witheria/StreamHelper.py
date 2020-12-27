import os
from inspect import getsourcefile

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from sys import platform

from pathlib import Path

home = str(Path.home())

print("Platform is " + platform, ", Home directory is " + home)
standardFilePath = "None"
symbol = "None"
if platform == "linux":
    try:
        os.mkdir(home + "/Documents/StreamHelper")
    except FileExistsError:
        print("\n")
    standardFilePath: str = home + "/Documents/StreamHelper"
    symbol: str = "/"
    system = 0
elif platform == "win64":
    standardFilePath: str = os.getenv('LOCALAPPDATA') + "\\StreamHelper"
    symbol: str = "\\"
    system = 0
elif platform == "win32":
    standardFilePath: str = os.getenv('LOCALAPPDATA') + "\\StreamHelper"
    symbol: str = "\\"
    system = 0

# Installation path, app id, product info
SOURCE_PATH: str = os.path.split(os.path.abspath(getsourcefile(lambda: 0)))[0].replace("runtime", "")
print(SOURCE_PATH)
APP_ID: str = "ToniSchmidbauer.StreamHelper.StreamHelperOpenAlpha.0.3.0"


# StyleSheet for the list elements
shortBorder = \
    ".QWidget {\n" \
    + "border: 1px solid black;\n" \
    + "}"

name = ""
count = 1

# States of the List Widgets
deselectItemFunctionInitiated = [False, False]
deselectListFunctionInitiated = False
lastListSelected = 0
lastItemSelected = [0, 0]

# Standard Filepath and File Names
# standardFilePath: str = os.getcwd()
# standardFileNames = {"chronoup", "chronodown", "time"} UNUSED
standardXMLNames = ['autosave', 'config', 'settings']
standardDirNames = ['Lists', 'eSports', 'API']
forbiddenChars = ["/", ">", "<", ":", "\"", "\\", "|", "?", "*", "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3",
                  "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                  "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

# Saving lists and values
saveLists = {"Left": None, "Right": None}
saveListNames = {}
saveListValues = {}
saveListItems = {"Left": {}, "Right": {}}
saveListData = {"Left": {}, "Right": {}}

# create all necessary lists
txtlist = {"CS_Day": "", "CS_Game": "", "CS_Group": "", "CS_League": "", "CS_Tournament": "",
           "HT_Player1": "", "HT_Player2": "", "HT_Player3": "", "HT_Player4": "", "HT_Player5": "",
           "HT_Sub1": "", "HT_Sub2": "", "HT_abbreviation": "", "HT_city": "", "HT_Comment": "",
           "HT_name": "", "HT_organisation": "",
           "T1_name": "", "T1_score": "", "T1_city": "",
           "T2_name": "", "T2_score": "", "T2_city": "",
           "T3_name": "", "T3_score": "", "T3_city": "",
           "T4_name": "", "T4_score": "", "T4_city": ""
           }
folderlist = ["Competitive Streaming", "Home Team", "Teams"]

lineedit_list = {}

# Standard autosave look
autosave_standard = {"Lists": saveListData, "eSports": {"txtlist": txtlist}}

# Setting settings
# Look for images at these locations (they have to be named according to the guidelines)
imageLocations = {"0": standardFilePath + symbol + "images"}

# Image names
imageNames = {

}

# Dict to process the settings tree and connect it to the stacked widget
settingsList = {
    "Main Settings": 0,
    "Riot API": 0,
    "File Paths": 1,
    "Lists": 2,
    "Miscellaneous": 3,
    "Riot Settings": 4,
    "Statistics": 5,
    "Timers": 6,
    "About": 6
}
# This list will be loaded on startup from the settings file, and saved on request or shutdown. Any changes will
# therefore apply immediately
configList = {
    # Basic settings
    "StartupTab": 0,
    "StartupSettingsTab": 0,

    # File path settings
    "UserFilePath": 0,
    "CustomFilePath": standardFilePath,
    "ImagePaths": imageLocations,

    # List settings
    "AllowedItems": {
        "Chrono Item": False,
        "GT Item": False,
        "Number Item": True,
        "Text Item": True
    },
    "GlobalPretext": "",
    "ListSplit": False,
    "AutoUpdateFiles": False,
    "RightListName": "Right",
    "LeftListName": "Left",

    # Riot API settings
    "FontSize": 11,
    "ChronoFormat": ""

}
# List used for resetting the settings (wont be changed around and read like the other one)
standardConfigList = {
    # Basic settings
    "StartupTab": 0,
    "StartupSettingsTab": 0,

    # File path settings
    "UserFilePath": 0,
    "CustomFilePath": standardFilePath,
    "ImagePaths": imageLocations,

    # List settings
    "AllowedItems": {
        "Chrono Item": False,
        "GT Item": False,
        "Number Item": True,
        "Text Item": True
    },
    "GlobalPretext": "",
    "ListSplit": False,
    "AutoUpdateFiles": False,
    "RightListName": "Right",
    "LeftListName": "Left",

    # Riot API settings
    "FontSize": 11,
    "ChronoFormat": ""

}

# This saves the currently active Summoner for the session
summoner = ""

# Stuff needed for eSports
# This is the path where all our actions will commence:
path = ""

# This is for creating the two folders if ListSplit is enabled:
ListSplitFolders = [configList["RightListName"], configList["LeftListName"]]

# This exists to allow the score operations to work
lastScoreChange = 0

# Since there are a lot of access requests to readAutosave(), only every % request will get logged
AUTOSAVE_LOG_LEVEL_OUTPUT = 4
