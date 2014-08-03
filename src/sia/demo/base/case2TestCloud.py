'''
Main

'''

import time
from random import random
from cloud import *
import matplotlib.pyplot as plt
import networkx as nx
from crr import *
from job import *

if __name__ == '__main__':
    # 1
    start = time.clock()
    c1 = Cloud(4, 2, 2, 4, 4, 4, 4, 4)
    #c2 = Cloud(2, 2, 2, 2, 2, 3, 3, 2, 2)

    # 2
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)
    #cloudList_for_job1.append(c2)

    # 3
    job1 = App(1, cloudList_for_job1)
    appList = []
    appList.append(job1)

    # 4
    cloudList = []
    cloudList.append(c1)
    #cloudList.append(c2)

    # 5
    crr = CRR(cloudList, appList)
    crr.build_fault_tree_for_app()

    counter = 0.0

    for i in range(0, 10000000):
        isHappen = crr.get_failure_of_app()
        if isHappen == 1:
            counter += 1.0
    print('result = %f'%(counter / 10000000.0))
    end = time.clock()
    print(end - start)
