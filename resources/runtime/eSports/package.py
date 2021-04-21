from resources.runtime import savestate
from resources.runtime.Settings.logfunctions import logWrite

from resources.runtime.Settings.save import readAutosave
from resources.runtime.eSports.program import saveCurrentState, loadTexts
from resources.runtime.textfiles.fileedit import editTxts, initTextFiles


def initPackage(ui):
    """
    This Method creates all necessary textfiles for the eSports-UI and connects the line edits to them.
    I'm splitting the main interface into three parts, so lag shouldn't be a large problem, even on slower PCs.

    :type ui: uic.load element
    :return: bool
    """
    logWrite("Initializing eSports tab...")
    # Add each lineedit to the list in savestate for ease of access
    temp_lineedit_list = {"CS_League": ui.CS_League,
                          "CS_Game": ui.CS_Game,
                          "CS_Day": ui.CS_Day,
                          "CS_Group": ui.CS_Group,
                          "CS_Tournament": ui.CS_Tournament,
                          "HT_Player1": ui.HT_Player1,
                          "HT_Player2": ui.HT_Player2,
                          "HT_Player3": ui.HT_Player3,
                          "HT_Player4": ui.HT_Player4,
                          "HT_Player5": ui.HT_Player5,
                          "HT_Sub1": ui.HT_Sub1,
                          "HT_Sub2": ui.HT_Sub2,
                          "HT_abbreviation": ui.HT_abbreviation,
                          "HT_city": ui.HT_city,
                          "HT_name": ui.HT_name,
                          "HT_organisation": ui.HT_organisation,
                          "HT_Comment": ui.HT_comment,
                          "T1_name": ui.T1_name,
                          "T1_score": ui.T1_score,
                          "T1_city": ui.T1_city,
                          "T2_name": ui.T2_name,
                          "T2_score": ui.T2_score,
                          "T2_city": ui.T2_city,
                          "T3_name": ui.T3_name,
                          "T3_score": ui.T3_score,
                          "T3_city": ui.T3_city,
                          "T4_name": ui.T4_name,
                          "T4_score": ui.T4_score,
                          "T4_city": ui.T4_city
                          }

    savestate.lineedit_list = temp_lineedit_list

    # Create the bonus folders to differentiate
    initTextFiles("initFolders")

    # ! REDUNDANT ! - Now in fileedit
    # try:
    #    print("Trying to create eSports folder...")
    #    for folder in folderlist:
    #        makedirs(path + savestate.symbol + folder)
    # except FileExistsError:
    #    print("eSports folders are already created!")
    # except PermissionError:
    #    print("This location requires elevated permissions")

    # Load a save
    logWrite("Trying to read the eSports autosave")
    lists = readAutosave("eSports")
    savestate.txtlist = lists["txtlist"]
    savestate.morelist = lists["morelist"]
    loadTexts()

    # Connect the lineedits to the textfiles
    # Write to textfiles

    # Competitive Streaming
    ui.CS_Day.editingFinished.connect(lambda: editTxts("CS_Day"))
    ui.CS_Game.editingFinished.connect(lambda: editTxts("CS_Game"))
    ui.CS_League.editingFinished.connect(lambda: editTxts("CS_League"))
    ui.CS_Group.editingFinished.connect(lambda: editTxts("CS_Group"))
    ui.CS_Tournament.editingFinished.connect(lambda: editTxts("CS_Tournament"))
    ui.showMoreFieldsButton.clicked.connect(lambda: showAddFields())

    # Home Team
    ui.HT_Player1.editingFinished.connect(lambda: editTxts("HT_Player1"))
    ui.HT_Player2.editingFinished.connect(lambda: editTxts("HT_Player2"))
    ui.HT_Player3.editingFinished.connect(lambda: editTxts("HT_Player3"))
    ui.HT_Player4.editingFinished.connect(lambda: editTxts("HT_Player4"))
    ui.HT_Player5.editingFinished.connect(lambda: editTxts("HT_Player5"))

    ui.HT_Sub1.editingFinished.connect(lambda: editTxts("HT_Sub1"))
    ui.HT_Sub2.editingFinished.connect(lambda: editTxts("HT_Sub2"))
    ui.HT_abbreviation.editingFinished.connect(lambda: editTxts("HT_abbreviation"))
    ui.HT_city.editingFinished.connect(lambda: editTxts("HT_city"))
    ui.HT_name.editingFinished.connect(lambda: editTxts("HT_name"))
    ui.HT_organisation.editingFinished.connect(lambda: editTxts("HT_organisation"))

    ui.HT_comment.textChanged.connect(lambda: editTxts("HT_Comment"))

    # Teams section
    ui.T1_name.editingFinished.connect(lambda: editTxts("T1_name"))
    ui.T1_score.editingFinished.connect(lambda: editTxts("T1_score"))
    ui.T1_city.editingFinished.connect(lambda: editTxts("T1_city"))
    ui.T2_name.editingFinished.connect(lambda: editTxts("T2_name"))
    ui.T2_score.editingFinished.connect(lambda: editTxts("T2_score"))
    ui.T2_city.editingFinished.connect(lambda: editTxts("T2_city"))
    ui.T3_name.editingFinished.connect(lambda: editTxts("T3_name"))
    ui.T3_score.editingFinished.connect(lambda: editTxts("T3_score"))
    ui.T3_city.editingFinished.connect(lambda: editTxts("T3_city"))
    ui.T4_name.editingFinished.connect(lambda: editTxts("T4_name"))
    ui.T4_score.editingFinished.connect(lambda: editTxts("T4_score"))
    ui.T4_city.editingFinished.connect(lambda: editTxts("T4_city"))

    # Clears
    ui.T_clear.clicked.connect(lambda: clearSection("T"))
    ui.HT_clear.clicked.connect(lambda: clearSection("HT"))
    ui.CS_clear.clicked.connect(lambda: clearSection("CS"))

    # Swaps
    ui.t1t2_swap.clicked.connect(lambda: swapTeams(0))
    ui.t3t4_swap.clicked.connect(lambda: swapTeams(1))
    ui.T_swap.clicked.connect(lambda: swapTeams(2))

    # Saves
    ui.T_save.clicked.connect(lambda: saveCurrentState())
    ui.T_saveNoEdit.clicked.connect(lambda: saveCurrentState())
    ui.CS_save.clicked.connect(lambda: saveCurrentState())
    ui.HT_toTeam.clicked.connect(lambda: saveCurrentState())

    # HT interactions
    ui.T1_setHT.clicked.connect(lambda: setHomeTeam(1))
    ui.T2_setHT.clicked.connect(lambda: setHomeTeam(2))
    ui.T3_setHT.clicked.connect(lambda: setHomeTeam(3))
    ui.T4_setHT.clicked.connect(lambda: setHomeTeam(4))

    # Score Interactions
    ui.t1_zero.clicked.connect(lambda: scoreInteraction("zero", 1, 0))
    ui.t2_zero.clicked.connect(lambda: scoreInteraction("zero", 2, 0))
    ui.t3_zero.clicked.connect(lambda: scoreInteraction("zero", 3, 0))
    ui.t4_zero.clicked.connect(lambda: scoreInteraction("zero", 4, 0))
    ui.T_ScoreDiff.valueChanged.connect(lambda: scoreInteraction("operation",
                                                                 int(ui.T_ScoreDiff.text()),
                                                                 ui.T_ScoreOperator.currentIndex()))
    ui.T_ScoreDiff.editingFinished.connect(lambda: zeroScoreChanger(ui))
    ui.T_ZeroScore.clicked.connect(lambda: scoreInteraction("zeroAll", 0, 0))


def clearSection(section):
    """
    This method sets all line edits and spin boxes within a section to zero or empty (HT, Teams or CS)

    :param section: str
    :return: None
    """
    # Telling the log whats up
    logWrite("Clearing section " + section)
    # initializing an array to check if everything went smoothly. every result gets appended here, so we know where
    success = []
    if section == "HT":
        for element in savestate.lineedit_list:
            if "HT_" in element:
                try:
                    # Try and set every line edit in the ui to the respective text
                    savestate.lineedit_list[element].setText("")
                    success.append(True)
                except KeyError as e:
                    # If we dont find one, there might be tampering going on
                    logWrite(f"{str(e)} was not found in the line edit list - Illegal Access Code")
                    print(str(e) + " not found!")
                    success.append(False)
                except AttributeError:
                    # This should happen if there is actually a spinbox instead of a line edit

                    try:
                        savestate.lineedit_list[element].setValue(0)
                    except KeyError as e:
                        logWrite(f"{str(e)} was not found in the spin box list - Illegal Access Code")
                        print(str(e) + " not found!")
    elif section == "CS":
        for element in savestate.lineedit_list:
            if "CS_" in element:
                try:
                    savestate.lineedit_list[element].setText("")
                    success.append(True)
                except KeyError as e:
                    logWrite("KeyError occurred while clearing section!")
                    print(str(e) + " not found!")
                    success.append(False)
                except AttributeError:
                    # This should happen if there is no lineedit ( SpinBox for score )

                    try:
                        savestate.lineedit_list[element].setValue(0)
                    except KeyError as e:
                        logWrite("KeyError occurred while clearing section (number)!")
                        print(str(e) + " not found!")
    else:
        for team in range(1, 5):
            try:
                savestate.lineedit_list["T" + str(team) + "_city"].setText("")
                savestate.lineedit_list["T" + str(team) + "_name"].setText("")
                savestate.lineedit_list["T" + str(team) + "_score"].setValue(0)
                success.append(True)
            except KeyError as e:
                logWrite("KeyError occurred while clearing teams!")
                print(str(e) + " not found!")
                success.append(False)
    if False in success:
        logWrite("The autosave seems to be incomplete or corrupted")
        print("The autosave seems to be incomplete or corrupted")
    editTxts("all")
    saveCurrentState()


def swapTeams(way):
    """
    To swap two teams, it is enough to set the text in the lineedits accordingly and then call editTxts()

    ""way" is the direction the teams should be swapped:

        0 = Swap T1 and T2

        1 = Swap T3 and T4

        2 = Swap T1, T2 and T3, T4

    :type way: int
    :return: None
    """

    if way == 0:
        logWrite("Swapping team 1 and 2.")
        element: str
        for element in savestate.lineedit_list:
            if "T1" in element:
                try:
                    temp = savestate.lineedit_list[element].text()
                except AttributeError:
                    temp = savestate.lineedit_list[element].value()
                try:
                    savestate.lineedit_list[element].setText(
                        savestate.lineedit_list["T2_" + str(element.replace("T1_", ""))].text())
                    savestate.lineedit_list["T2_" + str(element.replace("T1_", ""))].setText(temp)
                except AttributeError:
                    savestate.lineedit_list[element].setValue(
                        int(savestate.lineedit_list["T2_" + str(element.replace("T1_", ""))].text()))
                    savestate.lineedit_list["T2_" + str(element.replace("T1_", ""))].setValue(int(temp))
        editTxts("all")

    if way == 1:
        logWrite("Swapping team 3 and 4.")

        element: str
        for element in savestate.lineedit_list:
            if "T3" in element:
                try:
                    temp = savestate.lineedit_list[element].text()
                except AttributeError:
                    temp = savestate.lineedit_list[element].value()
                try:
                    savestate.lineedit_list[element].setText(
                        savestate.lineedit_list["T4_" + str(element.replace("T3_", ""))].text())
                    savestate.lineedit_list["T4_" + str(element.replace("T3_", ""))].setText(temp)
                except AttributeError:
                    savestate.lineedit_list[element].setValue(
                        int(savestate.lineedit_list["T4_" + str(element.replace("T3_", ""))].text()))
                    savestate.lineedit_list["T4_" + str(element.replace("T3_", ""))].setValue(int(temp))
        editTxts("all")

    if way == 2:
        logWrite("Swapping all teams.")
        for element in savestate.lineedit_list:
            if "T3" in element:
                try:
                    temp = savestate.lineedit_list[element].text()
                except AttributeError:
                    temp = savestate.lineedit_list[element].value()
                try:
                    savestate.lineedit_list[element].setText(
                        savestate.lineedit_list["T1_" + str(element.replace("T3_", ""))].text())
                    savestate.lineedit_list["T1_" + str(element.replace("T3_", ""))].setText(temp)
                except AttributeError:
                    savestate.lineedit_list[element].setValue(
                        int(savestate.lineedit_list["T1_" + str(element.replace("T3_", ""))].text()))
                    savestate.lineedit_list["T1_" + str(element.replace("T3_", ""))].setValue(int(temp))
            if "T4" in element:
                try:
                    temp = savestate.lineedit_list[element].text()
                except AttributeError:
                    temp = savestate.lineedit_list[element].value()
                try:
                    savestate.lineedit_list[element].setText(
                        savestate.lineedit_list["T2_" + str(element.replace("T4_", ""))].text())
                    savestate.lineedit_list["T2_" + str(element.replace("T4_", ""))].setText(temp)
                except AttributeError:
                    savestate.lineedit_list[element].setValue(
                        int(savestate.lineedit_list["T2_" + str(element.replace("T4_", ""))].text()))
                    savestate.lineedit_list["T2_" + str(element.replace("T4_", ""))].setValue(int(temp))
        editTxts("all")


def setHomeTeam(where):
    """
    This method is used to set a teams (determined by "where") city and name to the home teams'

    :param where: int
    :return: None
    """
    logWrite("Setting the home team to team " + str(where))
    savestate.lineedit_list["T" + str(where) + "_name"].setText(savestate.lineedit_list["HT_name"].text())
    savestate.lineedit_list["T" + str(where) + "_city"].setText(savestate.lineedit_list["HT_city"].text())
    editTxts("all")


def scoreInteraction(action: str, value: int, operator: int):
    """
    This method handles score interactions within the application.

    It is used to set the score to zero or handle the score operations.

    Input parameters should be as follows:

        action = can be "zero", "zeroAll" or "operation"

        value = specifies the team number for "zero" or is the
                value for the operation

        operator = not used for "zero", but specifies the
                    operator to use on the scores. Can be
                        0 for "+ value",
                        1 for "- value" or
                        2 for "set score to value"

    :param action: str
    :param value: int
    :param operator: int
    :return: None
    """

    logWrite("Commencing operation " + action + " with value " + str(value) + " and operator number " + str(operator))

    if action == "zero":
        savestate.lineedit_list["T" + str(value) + "_score"].setValue(0)
        editTxts(str("T" + str(value) + "_score"))

    if action == "zeroAll":
        for team in range(1, 5):
            savestate.lineedit_list["T" + str(team) + "_score"].setValue(0)
            editTxts("T" + str(team) + "_score")

    if action == "operation":
        print(savestate.lastScoreChange, value)
        if operator == 0:  # +
            if savestate.lastScoreChange > value:  # we need some way of saving the score
                savestate.lastScoreChange = value
            else:
                for team in range(1, 5):
                    currentValue = int(savestate.lineedit_list["T" + str(team) + "_score"].text()) - value + 1
                    savestate.lineedit_list["T" + str(team) + "_score"].setValue(currentValue + value)
                    editTxts("T" + str(team) + "_score")
                savestate.lastScoreChange = value

        if operator == 1:  # -
            if savestate.lastScoreChange > value:
                savestate.lastScoreChange = value
            else:
                for team in range(1, 5):
                    currentValue = int(
                        savestate.lineedit_list["T" + str(team) + "_score"].text()) + savestate.lastScoreChange
                    savestate.lineedit_list["T" + str(team) + "_score"].setValue(currentValue - value)
                    editTxts("T" + str(team) + "_score")
                savestate.lastScoreChange = value

        if operator == 2:  # Set
            if value != 0:
                for team in range(1, 5):
                    savestate.lineedit_list["T" + str(team) + "_score"].setValue(value)
                    editTxts("T" + str(team) + "_score")
    logWrite("Successfully executed operation!")


def zeroScoreChanger(window):
    """
    Sets all score spin boxes and exclusively them to zero
    """
    logWrite("Setting team scores to zero")
    window.T_ScoreDiff.setValue(0)
    for team in range(1, 5):
        editTxts("T" + str(team) + "_score")


def showAddFields():
    """
    Wrapper function to show the extra fields
    """
    savestate.ExtraFieldWidget.ui.show()
