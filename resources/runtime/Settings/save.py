import json
from json import JSONDecodeError

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite


def writeToAutosave(name, write):
    templist = savestate.autosave_standard
    try:
        templist = readAutosave()
        # print("Got ", templist)
    except JSONDecodeError:
        logWrite("Saving to autosave failed because the json could not be decoded!")
        print("There was a problem decoding the JSON. Please resort to a backup or try to fix it manually!")

    autosave = open(savestate.standardFilePath + savestate.symbol + "autosave.json", "w+", encoding="utf-8")

    templist[name] = write
    # print("Data saved without key!")

    autosave.write(json.dumps(templist, indent=4))
    autosave.close()


def readAutosave(*filterkey):
    """
    This method is globally used to get data from the autosave

    :type filterkey: str
    :return: dict
    """
    if savestate.AUTOSAVE_LOG_LEVEL_OUTPUT == 4:
        logWrite("Parsing autosave...")
        savestate.AUTOSAVE_LOG_LEVEL_OUTPUT -= 1
    else:
        if savestate.AUTOSAVE_LOG_LEVEL_OUTPUT == 0:
            savestate.AUTOSAVE_LOG_LEVEL_OUTPUT = 4
        else:
            savestate.AUTOSAVE_LOG_LEVEL_OUTPUT -= 1
    try:
        with open(savestate.standardFilePath + savestate.symbol + "autosave.json", "r", encoding="utf-8") as autosave:
            json_object = json.loads(autosave.read())
            autosave.close()
            if filterkey:
                try:
                    print("Seaching for key:", filterkey[0])
                    return json_object[filterkey[0]]
                except KeyError:
                    return json_object
                except TypeError:
                    print("Type error occurred while processing" + filterkey[0], json_object)
            else:
                if json_object:
                    print("Returning json object!")
                    return json_object
                else:
                    return savestate.autosave_standard
    except FileNotFoundError:
        print("Autosave not found. Try restarting the program. Continuing for now...")
        logWrite("Autosave not found. This is not a critical error and a new one will be created...")
        return savestate.autosave_standard
