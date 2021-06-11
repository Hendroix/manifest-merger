#Merger file.

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import os

directory = './manifests'
typesMap = {}

def getManifests():
    for filename in os.listdir(directory):
        if filename != 'package.xml' and filename.endswith('.xml'):
            buildConsolitdatedManifest(directory + '/' + filename)

def buildConsolitdatedManifest(filePath):
    tree = ET.parse(r'%s' % filePath)
    root = tree.getroot()
    for child in root.findall('types'):
        typeName = child.find('name').text
        if typeName not in typesMap:
            typesMap[typeName] = set()

        for member in child.iterfind('members'):
            typesMap[typeName].add(member.text)

def generateOutput(map):
    package = ET.Element('package')
    package.set('xmlns', 'http://soap.sforce.com/2006/04/metadata')
    
    for key in map:
        types = ET.SubElement(package, 'types')
        map[key] = sorted(map[key])
        
        for item in map[key]:
            members = ET.SubElement(types, 'members')
            members.text = item
            
        name = ET.SubElement(types, 'name')
        name.text = key

    tree = ElementTree(package)
    ET.indent(tree, space='    ', level=0)
    tree.write('./output/output.xml', encoding='utf-8', xml_declaration=True)
        
def main():
    getManifests()
    generateOutput(typesMap)
    
if __name__ == "__main__":
    main()