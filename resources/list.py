import xml.etree.ElementTree as ET

# create the file structure
from resources.runtime.savestate import standardFilePath

data = ET.Element('data')
items = ET.SubElement(data, 'filepath')
Customfilepath = ET.SubElement(items, 'Customfilepath')
Standardfilepath = ET.SubElement(items, 'Standardfilepath')
Customfilepath.set('filepath', standardFilePath)
Standardfilepath.set('filepath', standardFilePath)
Customfilepath.text = 'Custom User Filepath'
Standardfilepath.text = 'Serves as Backup and initiation'

# create a new XML file with the results
mydata = ET.tostring(data).decode('utf-8')
myfile = open("config.xml", "w")
myfile.write(mydata)


