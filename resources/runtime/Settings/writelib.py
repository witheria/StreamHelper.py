try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def readSettings():
    # This method reads the settings from the file on startup and writes them to the dict in savestate

