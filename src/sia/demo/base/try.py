import xml.dom.minidom
import sys
import getopt
from model_generator import *
from draw import *

if __name__ == "__main__":
    '''
    dom = xml.dom.minidom.parse('document1.xml')
    root = dom.documentElement
    myList = root.getElementsByTagName('datacenter')

    for node in myList:
        alist = node.getElementsByTagName('ID')
        print(int(alist[0].childNodes[0].nodeValue))
        alist = node.getElementsByTagName('failure')
        print(float(alist[0].childNodes[0].nodeValue))
    '''
    m = ModelGenerator('document1.xml')
    draw(m.topology.node[30000000001]['DATACENTER'].topology, "RACK")
