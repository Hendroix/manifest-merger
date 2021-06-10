#Merger file.

import xml.etree.ElementTree as ET
import os

directory = './manifests'
typesMap = {}

def getManifests():
    for filename in os.listdir(directory):
        if filename != 'package.xml' and filename.endswith('.xml'):
            print(filename)

def buildConsolidateManifest():
    tree = ET.parse('./manifests/package.xml')
    root = tree.getroot()
    for child in root.findall('types'):
        typeName = child.find('name')
        typeMembers = []
        for member in child.iterfind('members'):
            typeMembers.append(str(member.text))

        typesMap[typeName] = typeMembers

    print(typesMap)

getManifests()