'''
This is a test sample for clone function.

In this test sample, we only generate two different cloud providers
with some same infrastructures.  Moreover, we create an application
depending on the first cloud provider.

The purpose of this test sample is to check if our program could
generate the most basic scenario.

'''
import time
from draw import *
from random import random
from cloud import *
import matplotlib.pyplot as plt
import networkx as nx
from crr import *
from job import *

if __name__ == '__main__':

    # obtain the start time
    start = time.clock()

    # whether we want to generate cloud service with common dependencies
    typeCloud = "CORRELATION"
    
    # generate cloud service
    c1 = Cloud("CORRELATION", 3, 4, 4, 4, 4, 4, 4, 4)

    # 2
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)

    # 3
    typeService = "RACK"
    app = App(2, 2, typeService, cloudList_for_job1)
    appList = []
    appList.append(app)

    # 4
    cloudList = []
    cloudList.append(c1)

    # 5
    crr = CRR(cloudList, appList)
    algorithm = "Min"
    crr.build_fault_tree_for_app(algorithm)
    
    end = time.clock()
    print(end - start)
    
    # 6
    draw(crr.faultTree, typeService)
