import xml.dom.minidom
import sys
import getopt
from model_generator import *
from draw import *
from crr import *

if __name__ == "__main__":
   
    m = ModelGenerator('document1.xml')
    #draw(m.topology, "DATACENTER")
    crr = CRR(m.topology)
    crr.get_failure_of_app_via_mcs()
