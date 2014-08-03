#from xml.etree import ElementTree
#from xml.etree.ElementTree import Element

import networkx as nx
import xml.etree.ElementTree as ET
import sys
import getopt

doc = ET.parse(sys.argv[1])
root = doc.getroot()

for child in root.iter('list'):
    print child
    #for item in child.find('node'):
    #    print('component name: %s'%item.attrib['id'])
    
    
    
    #for item in child.findall(sys.argv[2]):
    #    print('%s: %s'%(sys.argv[2],item.text))
    #print("---------------------")

'''
if str(sys.argv[2]) == "vendor":    
    for child in root.iter('node'):
        print('component name: %s'%child.attrib['id'])
        for itemVendor in child.findall('vendor'):
            print('vendor: %s'%itemVendor.text)
        print("-----------------")

elif sys.argv[2] == "description":
    for child in root.iter('node'):
        print('component name: %s'%child.attrib['id'])
        for itemVendor in child.findall('description'):
            print('Description: %s'%itemVendor.text)
        print("-----------------")
else:
    pass
'''
