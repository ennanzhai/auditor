'''
Main

'''

from random import random
from cloud import *
import matplotlib.pyplot as plt
import networkx as nx
from crr import *
from job import *

if __name__ == '__main__':
    # 1
    c1 = Cloud(2, 2, 2, 2, 2, 3, 3, 2, 2)
    c2 = Cloud(2, 2, 2, 2, 2, 3, 3, 2, 2)

    # 2
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)
    cloudList_for_job1.append(c2)

    # 3
    job1 = App(1, cloudList_for_job1)
    appList = []
    appList.append(job1)

    # 4
    cloudList = []
    cloudList.append(c1)
    cloudList.append(c2)

    # 5
    crr = CRR(cloudList, appList)
    crr.build_fault_tree_for_app()
    #crr.get_failure_of_app()

    # 6
    colors = ['red', 'blue', 'yellow']
    G = crr.faultTree

    pos = { }

    i_for_dc = 0.0
    i_for_power = 0.0
    i_for_internet = 0.0
    i_for_job = 0.0

    nodelistDC = []
    nodelistPower = []
    nodelistInternet = []
    nodelistJob = []
    
    for node in G:
        if G.node[node].keys()[0] == 'JOB':
            pos[node] = (0.3 + i_for_job, 1.4)
            i_for_job += 8
            nodelistJob.append(node)
        elif G.node[node].keys()[0] == 'DATACENTER':
            pos[node] = (0.1 + i_for_dc, 1.0)
            i_for_dc += 10
            nodelistDC.append(node)
        elif G.node[node].keys()[0] == 'POWERSTATION':
            pos[node] = (0.5 + i_for_power, 0.6)
            i_for_power += 4.5
            nodelistPower.append(node)
        elif G.node[node].keys()[0] == 'INTERNET':
            pos[node] = (0.2 + i_for_internet, 0.2)
            i_for_internet += 11.0
            nodelistInternet.append(node)
        else:
            pass

    nx.draw(G, pos, node_color = colors, node_size = 300)
    #nx.draw(c1.topology)
    plt.show()  
