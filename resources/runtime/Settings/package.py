import json

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite


def readSettings(nocopy=0):
    """
    This method reads the settings from the config file on startup and writes them to the dict in savestate
    if the optional nocopy argument is 1, the settings dict from the file will not be copied, instead returned
    """
    try:
        with open(savestate.standardFilePath + savestate.symbol + "config.json", "r", encoding="utf-8") as file:
            json_object = json.loads(file.read())
            if nocopy == 1:
                return json_object
            savestate.configList = json_object
    except FileNotFoundError:
        print("No config file found! Restart the program. If this error persists, please contact the developer.")
        logWrite("No config file has been found!")


def updateSettings():
    """
    Write the current (modified) settings to the config file
    """
    try:
        file = open(savestate.standardFilePath + savestate.symbol + "config.json", "w+", encoding="utf-8")
        output = json.dumps(savestate.configList, sort_keys=True, indent=4)
        file.write(output)
        file.close()
    except FileNotFoundError:
        logWrite("No config file could be found!")
        print("No config file found! Restart the program. If this error persists, please contact the developer.")
