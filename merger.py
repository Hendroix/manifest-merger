#Merger file.

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import os
import re
import sys

directory = './manifest'
typesMap = {}    
validTypeNames = set()
errors = []
outputPath = './output/output.xml'

def validateMembersName(member, typeName, filePath):
    if typeName == 'LightningComponentBundle' and member[0].isupper():
        errors.append(member + ', is a LWC with named with Pascal Casing in: ' + filePath)
    
def cleanXML(path):
    package_file = open(path)
    package_content = package_file.read()
    package_content_new = re.sub(' xmlns="[^"]+"', '', package_content, count=1)
    package_file = open(path, 'w')
    package_file.write(package_content_new)
    package_file.close()

def setValidTypeNames():
    for filename in os.listdir(directory):
        if filename == 'package.xml':
            path = directory + '/' + filename
            cleanXML(path)
            tree = ET.parse(r'%s' % path)
            root = tree.getroot()
            for child in root.findall('types'):
                typeName = child.find('name').text
                validTypeNames.add(typeName)

def buildConsolitdatedManifest(filePath):
    cleanXML(filePath)
    tree = ET.parse(r'%s' % filePath)
    root = tree.getroot()
    for child in root.findall('types'):
        typeName = child.find('name').text
        if typeName in validTypeNames:
            if typeName not in typesMap:
                typesMap[typeName] = set()

            for member in child.iterfind('members'):
                validateMembersName(member.text, typeName, filePath)
                typesMap[typeName].add(member.text)
        else:
            errors.append(typeName + ' is not a valid type in: ' + filePath)
            
def getManifests():
    for filename in os.listdir(directory):
        if filename != 'package.xml' and filename.endswith('.xml'):
            buildConsolitdatedManifest(directory + '/' + filename)

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
    tree.write(outputPath, encoding='utf-8', xml_declaration=True)
    
def printErrors():
    if len(errors) > 0:
        print('WARNING ERROR OCCOURED DURING MERING, SEE BELOW:')
        for error in errors:
            print(error)
    
def main():
    setValidTypeNames()
    getManifests()
    generateOutput(typesMap)
    printErrors()
    
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('Usage Details: merger.py <targetmanifest>')
        sys.exit()
        
    outputPath = sys.argv[1]
    outputPath = sys.argv[1].rsplit('/', 1)[0]
    outputFile = sys.argv[1].rsplit('/', 1)[1]
    
    if os.path.isdir(outputPath):
        if outputFile.endswith('.xml'):
            outputPath = outputPath + '/' + outputFile;
            print(outputPath)
            main()
        else: 
            print('GIVEN FILE NOT XML', sys.argv[1])
            sys.exit()
    else:
        print('GIVEN PATH IS NOT A PATH', sys.argv[1])
        sys.exit()