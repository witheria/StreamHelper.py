import datetime

from resources.runtime import savestate
from resources.runtime.savestate import standardFilePath


def logCreate():
    """
    Creates a log at the standard location (standardfilepath + "StreamLog.log")
    """
    logname = savestate.symbol + "StreamLog.log"

    z = open(standardFilePath + logname, "w+")
    z.write("Log initialized on " + str(datetime.datetime.now(tz=None)) + "\n" + "\n")
    # str(datetime.datetime.year) + "-" +
    # str(datetime.month) + "-" +
    # str(datetime.day) + "-" +
    # str(datetime.datetime.hour) + "-" +
    # str(datetime.datetime.minute) + "-" +
    # str(datetime.datetime.second))


def logWrite(text: str):
    """
    Writes a string to the log as a new line. Adds the current time in front of the text
    :type text: str
    """
    now = datetime.datetime.now()
    logname = standardFilePath + savestate.symbol + "StreamLog.log"
    z = None
    try:
        z = open(logname, "a")
    except FileNotFoundError:
        logCreate()
        logWrite(text)
    z.write("\n" + now.strftime("%H:%M:%S") + ":   " + text)


def logWriteNoTime(text):
    """
    Write a string to the logfile without putting the current time in front of it
    :type text: str
    """
    logname = standardFilePath + savestate.symbol + "StreamLog.log"
    z = None
    try:
        z = open(logname, "a")
    except FileNotFoundError:
        logCreate()
        logWrite(text)
    z.write(text)
