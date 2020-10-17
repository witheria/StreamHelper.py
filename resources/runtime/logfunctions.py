import datetime

from resources.runtime import savestate
from resources.runtime.savestate import standardFilePath


def logCreate():
    logname = savestate.symbol + "StreamLog.log"

    z = open(standardFilePath + logname, "w+")
    z.write("Log initialized on " + str(datetime.datetime.now(tz=None)) + "\n" + "\n")
    # str(datetime.datetime.year) + "-" +
    # str(datetime.month) + "-" +
    # str(datetime.day) + "-" +
    # str(datetime.datetime.hour) + "-" +
    # str(datetime.datetime.minute) + "-" +
    # str(datetime.datetime.second))


def logWrite(text):
    now = datetime.datetime.now()
    logname = standardFilePath + savestate.symbol + "StreamLog.log"
    try:
        z = open(logname, "a")
    except FileNotFoundError:
        logCreate()
        logWrite(text)
    z.write("\n" + now.strftime("%H:%M:%S") + ":   " + text)


def logWriteNoTime(text):
    logname = standardFilePath + savestate.symbol + "StreamLog.log"
    try:
        z = open(logname, "a")
    except FileNotFoundError:
        logCreate()
        logWrite(text)
    z.write(text)