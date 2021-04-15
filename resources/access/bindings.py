import asyncio
import json
import threading
import time

from lcu_driver import Connector

from resources.runtime import savestate
from resources.runtime.functions import information

connector = Connector()


def disconnectClient():
    savestate.thread.running = False
    savestate.thread.join()
    print(savestate.thread.is_alive())


def initConnection(self):
    self.ui.establishConnection.clicked.connect(lambda: getClient(self))
    self.ui.A_disconnect.clicked.connect(lambda: disconnectClient())


def startConnection(self):
    savestate.thread = ConnectionThread(self, 1, "LCU Connector", 1)
    savestate.thread.start()


def getClient(self):
    # init method to call all subsequent functions. Will build up the stats.
    try:
        startConnection(self)
    except IndexError:
        # if there is no = in the found part
        information("Error in collecting process data!")
        self.ui.SummonerName.setStyleSheet("QLineEdit{background: lightred;}")
    except Exception as e:
        print(e)
    tryPollSummonerName(self)
    print(savestate.summoner)


def tryPollSummonerName(self):
    print("Polling summoner name...")
    while savestate.summoner == "":
        time.sleep(1)
        if savestate.summoner != "":
            self.ui.SummonerName.setText(savestate.summoner["displayName"])
            self.ui.SummonerName.setStyleSheet("QLineEdit{background: lightgreen;}")
            break
        else:
            self.ui.SummonerName.setStyleSheet("QLineEdit{background: red;}")


async def syncPicks(connection, champpick: dict) -> dict:
    """
    This method is used to cut down the json response to a more readable dict and remove unnecessary parts

    keeps:
        - Champion picked
        - Bans (extra)
        - Skins
        - assigned position
        - spells

    :param connection: An open LCU-Driver connection object
    :param champpick: input dictionary, expects a response from the lcu-driver
    :return: dict object with stuff listed above {"bans": all bans, "champpick": all other information}
    """
    bans: dict = {"bluebansID": champpick["bans"]["myTeamBans"],
                  "bluebans": [savestate.champIdMaps[str(x)] for x in champpick["bans"]["myTeamBans"] if x != 0],
                  "redbansID": champpick["bans"]["theirTeamBans"],
                  "redbans": [savestate.champIdMaps[str(x)] for x in champpick["bans"]["theirTeamBans"] if x != 0]}
    print(bans)

    teamPicks: dict = {
        "blueTeam": [
            {"Name": "",
             "ChampId": x["championId"],
             "Spells": [x["spell1Id"], x["spell2Id"]],
             "Position": x["assignedPosition"],
             "ChampionName": savestate.champIdMaps[str(x["championId"])],
             "Skin": x["selectedSkinId"],
             "SummonerId": x["summonerId"]
             }
            for x in champpick["myTeam"] if x["championId"] != 0],

        "redTeam": [
            {"Name": "",
             "ChampId": x["championId"],
             "Spells": [x["spell1Id"], x["spell2Id"]],
             "Position": x["assignedPosition"],
             "ChampionName": savestate.champIdMaps[str(x["championId"])],
             "Skin": x["selectedSkinId"],
             "SummonerId": x["summonerId"]
             }
            for x in champpick["theirTeam"] if x["championId"] != 0],
    }
    print(teamPicks)
    # get the name of the summoner from the lcu
    for part in teamPicks["blueTeam"]:
        summonerNameRequest = await connection.request(
            "get", f"/lol-summoner/v1/summoners/{part['SummonerId']}")
        temp = await summonerNameRequest.json()
        part["Name"] = temp["displayName"]
    for part in teamPicks["redTeam"]:
        summonerNameRequest = await connection.request(
            "get", f"/lol-summoner/v1/summoners/{part['SummonerId']}")
        temp = await summonerNameRequest.json()
        part["Name"] = temp["displayName"]
    print(teamPicks)
    returnable = {"bans": bans, "champpick": teamPicks}
    # dump the json to a file
    with open("current-rotation.json", "w+", encoding="utf-8") as file:
        json.dump(returnable, file, indent=4, ensure_ascii=False)
    return returnable


def startConnector():
    try:
        connector.start()
    except ConnectionRefusedError:
        print("No Client found...")
    except RuntimeError:
        # Already running
        print("The connector is already running!")
    return


async def stopConnector():
    try:
        await connector.stop()
    except Exception as e:
        print(e)
    return


class ConnectionThread(threading.Thread):
    def __init__(self, parent, threadId, name, counter):
        threading.Thread.__init__(self)

        self.connection = False
        self.parent = parent
        self.threadId = threadId
        self.name = name
        self.counter = counter
        self.running = True
        self.connector = Connector()

    def run(self):
        print(f"Starting {self.name}")
        while self.running:  # Do the main loop
            if not self.connection:  # activate the connector
                startConnector()
                self.connection = True
            time.sleep(1)
        print(f"Ending thread {self.name}")


@connector.ready
async def connect(connection):
    # check if the user is already logged into his account
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print('Please login to your account.')
    else:
        savestate.summoner = await summoner.json()
        print(f"Connected with summoner: \n{savestate.summoner}")


@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def championPickSession(connection, event):
    print(f'{event.data}')
    await syncPicks(connection, event.data)


@connector.close
async def disconnect(_):
    print('The client have been closed!')
