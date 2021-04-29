import json
import os
import shutil
from json.decoder import JSONDecodeError

from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite
from resources.runtime.Settings.save import readAutosave, writeToAutosave
from resources.runtime.eSports.program import loadTexts
from resources.runtime.functions import erroreasy
from resources.runtime.savestate import symbol as s
from resources.runtime.textfiles.folderedit import emptyDir


def copyImage(path: str, newName: str, slist: int):
    """
    This method copies an image from the original location to the working directory, with a new name

    path: the original image path
    newName: the name the copied image will carry
    slist: an integer telling what list the item accesses from
    """
    if savestate.configList["ListSplit"]:
        if slist == 0:  # Left list
            newPath = savestate.configList["CustomFilePath"] + savestate.symbol + "textfiles" + savestate.symbol + \
                      "Lists" + savestate.symbol + savestate.configList["LeftListName"] + savestate.symbol + newName
            if not os.path.isfile(newPath):
                shutil.copy(path, newPath)
        elif slist == 1:  # Right list
            newPath = savestate.configList["CustomFilePath"] + savestate.symbol + "textfiles" + savestate.symbol + \
                      "Lists" + savestate.symbol + savestate.configList["RightListName"] + savestate.symbol + newName
            if not os.path.isfile(newPath):
                shutil.copy(path, newPath)
    else:
        newPath = savestate.configList["CustomFilePath"] + savestate.symbol + \
                    "textfiles" + savestate.symbol + "Lists" + savestate.symbol + newName
        shutil.copy(path, newPath)


def createListFiles(*load: str):
    """
    This method recreates the list files from the autosave.json file or a savefile

    :param load: str
    :return: None
    """
    loadFileCheck = ""
    if load is not None:
        loadFileCheck = load

    print("Trying to open the savefile...")
    logWrite("Trying to open the savefile...")

    # Lets look in the json so we know what was up
    try:
        # print(savestate.standardFilePath)
        if len(loadFileCheck) > 0:
            print("Fetching save file from: ", load)
            logWrite("Fetching save file from: " + str(load))
            json_object = json.loads(open(load[0], "r", encoding="utf-8").read())
        else:
            json_object = readAutosave()

        # After parsing we need to get the values for each field. Then we put it in the list.
        # Make sure that every ChronoItem is turned off

        # Lists
        for key in json_object["Lists"]["Left"]:
            savestate.saveListData["Left"][int(key)] = json_object["Lists"]["Left"][key]
            if "chronotype" in savestate.saveListData["Left"][int(key)]["itemData"]:
                savestate.saveListData["Left"][int(key)]["itemData"]["running"] = False
        for key in json_object["Lists"]["Right"]:
            savestate.saveListData["Right"][int(key)] = json_object["Lists"]["Right"][key]
            if "chronotype" in savestate.saveListData["Right"][int(key)]["itemData"]:
                savestate.saveListData["Right"][int(key)]["itemData"]["running"] = False

        # eSports

        # check if this is a valid list
        success = True
        # print("json object = ", json_object["eSports"])
        # print("txtlist = ", savestate.txtlist)
        for key in savestate.txtlist:
            if key not in json_object["eSports"]["txtlist"]:
                print("The autosave does not contain: " + key, ". Stopped loading!")
                logWrite("The autosave does not contain: " + key + ". Stopped loading!")
                success = False
                break
        if success:
            # Save it to the savestate
            savestate.txtlist = json_object["eSports"]["txtlist"]
            # print(savestate.txtlist)
            loadTexts()
            editTxts("all")
    except FileNotFoundError:
        print("No autosave.json file found! Please restart the program")
        logWrite("Autosave missing! Please restart the program!")
    except JSONDecodeError:
        print("Not able to decode the file! JSON Decode Error thrown!")
        logWrite("Autosave not readable in instance \"createListFiles\"! This error should never occur!")
        erroreasy("There was an error reading the old savefile! Please try to recover it or resort to a backup",
                  0x0103)

    # last but not least, update every item and create the new files
    getTextOfItem()
    # print(savestate.saveListData)
    from resources.runtime.textlists.program import updateLists
    updateLists()


def editTxts(name):
    """
    Used to update the textfiles connected to the lineedits in the eSports tab

    :param name: str
    :return: bool
    """
    # Edit the list which contains this name
    # print("Creating: ", name)
    # Update the textfiles
    if name == "all":
        for lineedit in savestate.txtlist:
            # print("Creating file: " + lineedit)

            editTxts(lineedit)
        return True
    elif name == "HT_Comment":
        savestate.txtlist[name] = savestate.lineedit_list[name].toPlainText()
        # print("Comment accepted")
        args = ["eSports",
                "comment",
                savestate.txtlist[name],
                "Home Team"
                ]
        # print("Comment here: ", args)
        initTextFiles("createFile", args)
        return True
    else:
        if "CS" in name:
            folder = "Competitive Streaming"
        elif "HT" in name:
            folder = "Home Team"
        else:
            folder = "Teams"
        try:
            if name != "HT_Comment":
                savestate.txtlist[name] = savestate.lineedit_list[name].text()
            else:
                savestate.txtlist[name] = savestate.lineedit_list[name].toPlainText()
            if folder == "Teams":
                args = ["eSports",
                        name.replace("T", "Team "),
                        savestate.txtlist[name],
                        folder
                        ]
            else:
                args = ["eSports",
                        name.replace(name.split("_")[0], "").replace("_", ""),
                        savestate.txtlist[name],
                        folder
                        ]
            initTextFiles("createFile", args)
        except KeyError:
            print("This name does not exist")
            # should be irrelevant but oh well


def getTextOfItem():
    """
    This method will update every item (if it exists), creates them otherwise, then writes all the data into the
    autosave file and creates all textfiles needed

    :return: None
    """
    # Just copy the saved items in the array from savestate into the file. Update all first though
    handling = 0
    check = 0
    # print(savestate.saveListData)
    try:
        for index in savestate.saveListData["Left"]:
            handling = index
            # Get the current element on index
            savestate.saveListData["Left"][index]["itemData"] = \
                savestate.saveListItems["Left"][index]["item"].getProperties()
            savestate.saveListItems["Left"][index]["item"].setEdit(savestate.configList["AutoUpdateFiles"])
        for index in savestate.saveListData["Right"]:
            # Get the current element on index
            handling = index
            savestate.saveListData["Right"][index]["itemData"] = \
                savestate.saveListItems["Right"][index]["item"].getProperties()
            savestate.saveListItems["Right"][index]["item"].setEdit(savestate.configList["AutoUpdateFiles"])
    except KeyError:
        # The first time we load up the list, there can't be any items in there
        # print("KeyError occurred at " + str(handling) + ". This is an expected error the first time the program is "
        #                                                 "loaded.")
        # print(savestate.saveListData)
        # print(savestate.saveListItems)
        logWrite("KeyError occurred at " + str(handling) + ". This is an expected error the first time the program is "
                                                           "loaded.")
    except RuntimeError:
        # Expected error the first time this is loaded
        print("Got an expected RuntimeError in getTextOfItem(). Please contact the developer if you see this message"
              " more than once.")
        pass
    try:
        if savestate.saveLists["Left"].count() == 0 and savestate.saveLists["Right"].count() == 0:
            tempArray = savestate.saveListData
            savestate.saveListItems = {"Left": {}, "Right": {}}
        else:
            # put the savestate array into the json
            tempArray = savestate.saveListData
            # print(tempArray)
    except AttributeError:
        # If the lists aren't saved yet
        tempArray = savestate.saveListData
    # print("Temp array is: ", tempArray)
    writeToAutosave("Lists", tempArray)
    lname = savestate.configList["LeftListName"]
    rname = savestate.configList["RightListName"]

    # create the textFiles
    try:
        for key in savestate.saveListData:

            thisname = lname
            if key == "Right":
                thisname = rname

            for index in savestate.saveListData[key]:
                now = savestate.saveListData[key][index]["itemData"]
                # print(now)

                if "pretext" in now:  # Number items
                    arg = ["Lists", now["name"], str(now["pretext"] + str(now["value"])), thisname]
                    check = initTextFiles("createFile", arg)
                elif "chronotype" in now:
                    # Chronoitems edit their own text files in real time (hehe, time lol)
                    pass

                elif "path" in now:
                    # Image items dont have any textfiles, we do call the update function though
                    savestate.saveListItems[key][index]["item"].copyPicture()
                else:
                    arg = ["Lists", now["name"], str(now["value"]), thisname]
                    check = initTextFiles("createFile", arg)
                if check > 0:
                    print("Item not accepted: ", savestate.saveListData[key][index])
    except KeyError as e:
        print(e)


def initTextFiles(access_token: str, *args):
    """
    !!! Another one of the "simplifications" !!!

    centralizes textfile creating and editing and other stuff like initializing all the files

    Error codes are:
        0 = Everything went smoothly, no errors

        1 = There was an Error somewhere (gets printed), the textfile could be created though

        2 = There was an Error somewhere (gets printed) and the file could NOT be created

        3 = Critical Failure, the function could not execute (either gets printed or the program dies)

    ARGS ARE REQUIRED FOR THESE OPERATIONS: "createFolder", "createFile", "deleteFile" \n
        Creating a folder:  arg = [String mode, String name, optional: String parentFolder]

        Creating a file:    arg = [String mode, String name, String text, optional: String parentFolder]

        Deleting a file:    arg = [String mode, String name, optional: String parentFolder]

        \nmode can be seen as where you want the file/folder to be. E.g.: mode="eSports" adds "eSports" to path
    There is no need to go deeper than two levels in this folder structure - yet

    :param access_token: String
    :return: int
    """
    if access_token == "initFolders":
        logWrite("Initializing Folders...")
        # Folder creation: Which folders need to be created?
        folder_list_esports = savestate.folderlist
        folder_list = savestate.standardDirNames

        # Where do they need to be created?
        folder_path = savestate.configList["CustomFilePath"] + s + "textfiles"

        # Check if they exist already and create them if they don't
        for folder in folder_list:
            path_to_folder = str(folder_path + s + folder)
            if not os.path.exists(path_to_folder):
                try:
                    os.mkdir(path_to_folder)
                except FileNotFoundError:
                    erroreasy("The path directory could not be found. It has been reset...", 0x0310)
                    savestate.configList["CustomFilePath"] = savestate.standardFilePath
            else:
                print("Directory already exists: " + folder)

        # Do the same for the subfolders
        try:
            for folder in folder_list_esports:
                path_to_folder = str(folder_path + s + "eSports" + s + folder)
                if not os.path.exists(path_to_folder):
                    os.mkdir(path_to_folder)
                else:
                    print("Directory already exists: " + folder)
        except FileNotFoundError:
            print("The folder \" eSports \" does not exist!")
            logWrite("The folder \"eSports\" does not exist!")
            return 2

        # Check for list split argument and delete the old folder
        if savestate.configList["ListSplit"]:
            logWrite("Creating split folders...")
            path_to_list_folder = ["left", "right"]
            if len(savestate.NewListName) >= 1:
                if savestate.NewListName[1] == 1:
                    print("Deleting old left folder and creating new one...")
                    emptyDir(folder_path + s + "Lists" + s + savestate.configList["LeftListName"])
                    savestate.configList["LeftListName"] = savestate.NewListName[0]
                elif savestate.NewListName[1] == 0:
                    print("Deleting old right folder and creating new one...")
                    emptyDir(folder_path + s + "Lists" + s + savestate.configList["RightListName"])
                    savestate.configList["RightListName"] = savestate.NewListName[0]
                else:
                    # if there was no other folder before the change
                    pass

            path_to_list_folder[0] = str(folder_path + s + "Lists" + s + savestate.configList["LeftListName"])
            path_to_list_folder[1] = str(folder_path + s + "Lists" + s + savestate.configList["RightListName"])
            for folder in path_to_list_folder:
                if not os.path.exists(folder):
                    try:
                        os.makedirs(folder)
                    except FileNotFoundError as e:
                        print(e)
                else:
                    print("List-splitting enabled and folder found: " + folder)
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    # print("Trying to delete: ", file_path)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                        logWrite(str('Failed to delete %s. Reason: %s' % (file_path, e)))
                        return 2

        # We need to make sure that the List folder(s) are empty because otherwise there will be leftovers
        folder = folder_path + s + "Lists"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                if os.path.isdir(file_path) and not savestate.configList["ListSplit"]:
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                logWrite(str('Failed to delete %s. Reason: %s' % (file_path, e)))
                return 2

        # Create the basic textfiles needed for operation
        createListFiles()
        return 0

    if access_token == "createFolder":
        logWrite("Creating a new folder...")
        if len(args) > 2:
            os.mkdir(savestate.configList["CustomFilePath"] + s + args[0] + s + args[2] + s + args[1])
            return 0
        else:
            os.mkdir(savestate.configList["CustomFilePath"] + s + args[0] + s + args[1])
            return 0

    if access_token == "createFile":
        args = args[0]
        # print(args)
        # print(savestate.configList["ListSplit"])
        # logWrite("Creating a new file with name " + args[1] + "...")
        if args[0] == "Lists":
            if savestate.configList["ListSplit"]:  # This will give a special thingy to the parent folder
                file_path: str = str(savestate.configList["CustomFilePath"] + s + "textfiles" + s + args[0]
                                     + s + args[3] + s + args[1] + ".txt")

            else:
                file_path: str = str(savestate.configList["CustomFilePath"] + s + "textfiles" + s + args[0]
                                     + s + args[1] + ".txt")
        else:
            if len(args) == 3:
                # No parent given
                file_path: str = str(savestate.configList["CustomFilePath"] + s + "textfiles" + s + args[0]
                                     + s + args[1] + ".txt")
            else:
                # Parent given
                file_path: str = str(savestate.configList["CustomFilePath"] + s + "textfiles" + s + args[0]
                                     + s + args[3] + s + args[1] + ".txt")

        # print("Creating a file here: ", file_path)
        try:
            with open(file_path, "w+", encoding="utf-8") as f:
                f.write(args[2])
        except FileNotFoundError:
            print("The folders have been deleted! Rebuilding them...")
            logWrite("The folders have been deleted while running! Rebuilding them...")
            initTextFiles("initFolders")
    return 0
