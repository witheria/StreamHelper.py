from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.Settings.save import writeToAutosave


def saveCurrentState():
    """
    Saves the lists to the autosave file

    :return: None
    """
    logWrite("Saving contents to the autosave...")
    thisSave = {
        "txtlist": savestate.txtlist,
        "morelist": savestate.morelist
    }
    writeToAutosave("eSports", thisSave)


def loadTexts():
    """
    Synchronizes the list data in savestate with the content of the line edits or spin boxes
    """
    success = []
    for element in savestate.lineedit_list:
        try:
            savestate.lineedit_list[element].setText(savestate.txtlist[element])
            success.append(True)
        except KeyError as e:
            logWrite("Error occurred while loading texts from the savestate!")
            print(str(e) + " not found!")
            success.append(False)
        except AttributeError:
            # This should happen if there is no lineedit ( SpinBox for score )
            try:
                savestate.lineedit_list[element].setValue(int(savestate.txtlist[element]))
            except KeyError as e:
                logWrite("Error occurred while loading texts from the savestate!")
                print(str(e) + " not found!")
            except ValueError:
                # Happens when the program is opened up the first time
                pass
    if False in success:
        print("The autosave seems to be incomplete or corrupted")
