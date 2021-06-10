#Merger file.

import xml.etree.ElementTree as ET
import os

directory = './manifests'
typesMap = {}

def getManifests():
    for filename in os.listdir(directory):
        if filename != 'package.xml' and filename.endswith('.xml'):
            print(filename)
            buildConsolitdatedManifest(directory + '/' + filename)

def buildConsolitdatedManifest(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    for child in root.findall('types'):
        typeName = child.find('name').text
        for member in child.iterfind('members'):
            typesMap[typeName][member.text]

getManifests()
print(typesMap)