import os
from inspect import getsourcefile

from PyQt5.QtCore import QTimer

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
APP_ID: str = "ToniSchmidbauer.StreamHelper.StreamHelperOpenAlpha.0.3.0"

# StyleSheet for the list elements
shortBorder = \
    ".QWidget {\n" \
    + "border: 1px solid black;\n" \
    + "}"

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
morelist = {"Caster1": "",
            "Caster2": "",
            "Caster3": "",
            "Stat1": "",
            "Stat2": "",
            "Stat3": "",
            "Custom1": "",
            "Custom2": "",
            "Custom3": "",
            }
folderlist = ["Competitive Streaming", "Home Team", "Teams", "More fields"]

lineedit_list = {}

# Standard autosave look
autosave_standard = {"Lists": saveListData, "eSports": {"txtlist": txtlist, "morelist": morelist}}

# Setting settings
# Look for images at these locations (they have to be named according to the guidelines)
imageLocations = {"0": standardFilePath + symbol + "images"}

# Image names
imageNames = {

}

# On changing list names, this will process the name so the old folder gets deleted
NewListName = tuple()

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
        "Chrono Item": True,
        "GT Item": False,
        "Number Item": True,
        "Text Item": True,
        "Image Item": True
    },
    "GlobalPretext": "",
    "ListSplit": False,
    "AutoUpdateFiles": False,
    "RightListName": "Right",
    "LeftListName": "Left",

    # eSport Settings
    "funnelfile_separator": "\n",

    # Riot API settings
    "FontSize": 11,
    "ChronoFormat": "hh:mm:ss"

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
        "Chrono Item": True,
        "GT Item": False,
        "Number Item": True,
        "Text Item": True,
        "Image Item": True
    },
    "GlobalPretext": "",
    "ListSplit": False,
    "AutoUpdateFiles": False,
    "RightListName": "Right",
    "LeftListName": "Left",

    # eSport Settings
    "funnelfile_separator": "\n",

    # Riot API settings
    "FontSize": 11,
    "ChronoFormat": "hh:mm:ss"

}

# This integer counts how many times the function saveChronoToAutosave in textlists.program has been accessed
chrono_access_counter: int = 0

# This saves the currently active Summoner for the session
summoner = ""

# Stuff needed for eSports

# This exists to allow the score operations to work
lastScoreChange = 0

# Since there are a lot of access requests to readAutosave(), only every %s request will get logged
AUTOSAVE_LOG_LEVEL_OUTPUT = 4

# This is the timer to clock the chronoitems
timer: QTimer = None

# Create the bonus fields window and connect it
ExtraFieldWidget = None

# important mappings for the League API
champIdMaps: dict = {
    "266": "Aatrox",
    "103": "Ahri",
    "84": "Akali",
    "12": "Alistar",
    "32": "Amumu",
    "34": "Anivia",
    "1": "Annie",
    "523": "Aphelios",
    "22": "Ashe",
    "136": "AurelionSol",
    "268": "Azir",
    "432": "Bard",
    "53": "Blitzcrank",
    "63": "Brand",
    "201": "Braum",
    "51": "Caitlyn",
    "164": "Camille",
    "69": "Cassiopeia",
    "31": "Chogath",
    "42": "Corki",
    "122": "Darius",
    "131": "Diana",
    "119": "Draven",
    "36": "DrMundo",
    "245": "Ekko",
    "60": "Elise",
    "28": "Evelynn",
    "81": "Ezreal",
    "9": "Fiddlesticks",
    "114": "Fiora",
    "105": "Fizz",
    "3": "Galio",
    "41": "Gangplank",
    "86": "Garen",
    "150": "Gnar",
    "79": "Gragas",
    "104": "Graves",
    "120": "Hecarim",
    "74": "Heimerdinger",
    "420": "Illaoi",
    "39": "Irelia",
    "427": "Ivern",
    "40": "Janna",
    "59": "JarvanIV",
    "24": "Jax",
    "126": "Jayce",
    "202": "Jhin",
    "222": "Jinx",
    "145": "Kaisa",
    "429": "Kalista",
    "43": "Karma",
    "30": "Karthus",
    "38": "Kassadin",
    "55": "Katarina",
    "10": "Kayle",
    "141": "Kayn",
    "85": "Kennen",
    "121": "Khazix",
    "203": "Kindred",
    "240": "Kled",
    "96": "KogMaw",
    "7": "Leblanc",
    "64": "LeeSin",
    "89": "Leona",
    "876": "Lillia",
    "127": "Lissandra",
    "236": "Lucian",
    "117": "Lulu",
    "99": "Lux",
    "54": "Malphite",
    "90": "Malzahar",
    "57": "Maokai",
    "11": "MasterYi",
    "21": "MissFortune",
    "62": "MonkeyKing",
    "82": "Mordekaiser",
    "25": "Morgana",
    "267": "Nami",
    "75": "Nasus",
    "111": "Nautilus",
    "518": "Neeko",
    "76": "Nidalee",
    "56": "Nocturne",
    "20": "Nunu",
    "2": "Olaf",
    "61": "Orianna",
    "516": "Ornn",
    "80": "Pantheon",
    "78": "Poppy",
    "555": "Pyke",
    "246": "Qiyana",
    "133": "Quinn",
    "497": "Rakan",
    "33": "Rammus",
    "421": "RekSai",
    "526": "Rell",
    "58": "Renekton",
    "107": "Rengar",
    "92": "Riven",
    "68": "Rumble",
    "13": "Ryze",
    "360": "Samira",
    "113": "Sejuani",
    "235": "Senna",
    "147": "Seraphine",
    "875": "Sett",
    "35": "Shaco",
    "98": "Shen",
    "102": "Shyvana",
    "27": "Singed",
    "14": "Sion",
    "15": "Sivir",
    "72": "Skarner",
    "37": "Sona",
    "16": "Soraka",
    "50": "Swain",
    "517": "Sylas",
    "134": "Syndra",
    "223": "TahmKench",
    "163": "Taliyah",
    "91": "Talon",
    "44": "Taric",
    "17": "Teemo",
    "412": "Thresh",
    "18": "Tristana",
    "48": "Trundle",
    "23": "Tryndamere",
    "4": "TwistedFate",
    "29": "Twitch",
    "77": "Udyr",
    "6": "Urgot",
    "110": "Varus",
    "67": "Vayne",
    "45": "Veigar",
    "161": "Velkoz",
    "254": "Vi",
    "234": "Viego",
    "112": "Viktor",
    "8": "Vladimir",
    "106": "Volibear",
    "19": "Warwick",
    "498": "Xayah",
    "101": "Xerath",
    "5": "XinZhao",
    "157": "Yasuo",
    "777": "Yone",
    "83": "Yorick",
    "350": "Yuumi",
    "154": "Zac",
    "238": "Zed",
    "115": "Ziggs",
    "26": "Zilean",
    "142": "Zoe",
    "143": "Zyra"
}
