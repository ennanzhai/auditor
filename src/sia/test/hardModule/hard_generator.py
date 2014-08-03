#from xml.etree import ElementTree
#from xml.etree.ElementTree import Element
import networkx as nx
import xml.etree.ElementTree as ET

doc = ET.parse("hard-3.xml")
root = doc.getroot()

'''
for child in root.iter('node'):
    print('component name: %s'%child.attrib['id'])
    for itemVendor in child.findall('vendor'):
        print('vendor: %s'%itemVendor.text)
    print("-----------------")
'''

for child in root.iter('node'):
    print('component name: %s'%child.attrib['id'])
    for itemVendor in child.findall('description'):
        print('Description: %s'%itemVendor.text)
    print("-----------------")


