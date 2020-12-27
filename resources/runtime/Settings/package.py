import json

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite


def readSettings():
    # This method reads the settings from the file on startup and writes them to the dict in savestate
    logWrite("Loading contents from savefile...")

    try:
        file = open(savestate.standardFilePath + savestate.symbol + "config.json", "r", encoding="utf-8")
        json_object = json.loads(file.read())
        savestate.configList = json_object
        file.close()
    except FileNotFoundError:
        logWrite("No config file could be found!")
        print("No config file found! Restart the program. If this error persists, please contact the developer.")


def updateSettings():
    try:
        file = open(savestate.standardFilePath + savestate.symbol + "config.json", "w+", encoding="utf-8")
        output = json.dumps(savestate.configList, sort_keys=True, indent=4)
        file.write(output)
        file.close()
    except FileNotFoundError:
        logWrite("No config file could be found!")
        print("No config file found! Restart the program. If this error persists, please contact the developer.")
