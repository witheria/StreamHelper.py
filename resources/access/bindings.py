import re
import subprocess

from lcu_driver import Connector

from resources.images.program import copyFile
from resources.runtime import savestate

connector = Connector()


def initConnection(self):
    self.ui.establishConnection.clicked.connect(lambda: getClient(self))
    self.ui.swapTeams.clicked.connect(lambda: copyFile(
        "F:\\Windows Installation\\Bilder\\test.jpg",
        "C:\\Program Files\\obs-studio\\bin\\64bit\\LCS-Champ-Select.jpg"))


def getClient(self):
    # init method to call all subsequent functions. Will build up the stats.
    try:
        cmdrun = subprocess.run(['wmic', 'PROCESS', "WHERE", "name='LeagueClientUx.exe'", "GET", "commandline"],
                            capture_output=True, text=True).stdout
    except AttributeError:
        print("Process not found!")
    try:
        port = re.search("app-port=([0-9]*)", cmdrun).group().split("=")[1]
        auth = re.search("remoting-auth-token=([\w]*)", cmdrun).group().split("=")[1]
    except IndexError:
        # if there is no = in the found part
        port = "Error in collecting process data!"
        auth = ""
        self.ui.SummonerName.setStyleSheet("QLineEdit{background: lightred;}")
    except AttributeError:
        # if the client isn't open
        port = "Please make sure that you have your League Client up and running!"
        auth = ""
        self.ui.SummonerName.setStyleSheet("QLineEdit{background: lightred;}")
    print(port, auth)

    try:
        startConnector()
    except:
        print("nothing found")
    if savestate.summoner != "":
        self.ui.SummonerName.setText(savestate.summoner["displayName"])
        self.ui.SummonerName.setStyleSheet("QLineEdit{background: lightgreen;}")
    else:
        self.ui.SummonerName.setStyleSheet("QLineEdit{background: red;}")


def startConnector():
    @connector.ready
    async def connect(connection):
        # check if the user is already logged into his account
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
        if summoner.status != 200:
            print('Please login to your account.')
        else:
            print('Summoner received successfully!')
            savestate.summoner = await summoner.json()
            print(savestate.summoner["displayName"])

    @connector.close
    async def disconnect(_):
        print('Finished task')
        await connect.stop()

    try:
        connector.start()
    except ConnectionRefusedError:
        print("No Client found...")