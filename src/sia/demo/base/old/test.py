'''


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
    # If you assign "GOOD" to typeCloud, we will obtain a cloud without
    # hidden common dependencies
    # If you assign "CORRELATION" to typeCloud, we will obtain a cloud
    # with hidden common dependencies
    
    typeCloud = "CORRELATION"
    
    # generate cloud service
    # The parameters are :
    # 1. cloud type --- without common dependencies or with
    # 2. the # of data centers
    # 3. the # of core routers
    # 4. the # of agg switches
    # 5. the # of racks
    # 6. the # of powers assigned to each data center
    # 7. the # of powers the cloud service totally has
    # 8. the # of Internet routers assigned to each data center
    # 9. the # of Internet routers the cloud service totally has
    
    c1 = Cloud(typeCloud, 2, 2, 2, 2, 2, 2, 2, 2)

    # initializing application
    
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)

    # The layer of the service we are focusing on
    # There are two types of layers, i.e., data center and rack
    # If we assign "RACK" to typeService, we will go into a given data
    # center.
    # If we assign "DATACENTER" to typeService, we will focus on
    # a given cloud with many data centers
    
    typeService = "RACK"
    app = App(1, 3, typeService, cloudList_for_job1)
    appList = []
    appList.append(app)

    # 4
    cloudList = []
    cloudList.append(c1)

    # Since CRA has different types of algorithms:
    # "MC" means we are using Monte Carlo algorithm
    # The numbers of trials are set in the configuration.py file
    # The variable of trials is "TRIALS"
    # 
    crr = CRR(cloudList, appList)
    algorithm = "Minimal"
    crr.build_fault_tree_for_app(algorithm)
    
    end = time.clock()
    print(end - start)
    
    # 6
    draw(crr.faultTree, typeService)
