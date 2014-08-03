'''
This is a test sample for clone function.

In this test sample, we only generate two different cloud providers
with some same infrastructures.  Moreover, we create an application
depending on the first cloud provider.

The purpose of this test sample is to check if our program could
generate the most basic scenario.

'''
import time
from random import random
from cloud import *
import matplotlib.pyplot as plt
import networkx as nx
from crr_mcs import *
from job import *

if __name__ == '__main__':
    # 1
    start = time.clock()

    # 1 data center
    # 2 core routers
    # 2 agg switches
    # 4 racks
    c1 = Cloud(3, 10, 20, 20, 2, 2, 2, 2)

    # 2
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)

    # 3
    job1 = App(1, cloudList_for_job1)
    appList = []
    appList.append(job1)

    # 4
    cloudList = []
    cloudList.append(c1)

    # 5
    crr = CRR(cloudList, appList)
    crr.build_fault_tree_for_app()
    crr.get_failure_of_app()
    
    end = time.clock()
    print('The costed time is:  %f'%(end - start))
    '''
    G = crr.faultTree
    pos = { }
    labels = {}

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
            nodelistJob.append(node)
            pos[node] = (10 + i_for_job, 14)
            labels[node] = r'APP'
            i_for_job += 8
        if G.node[node].keys()[0] == 'DATACENTER':
            pos[node] = (5 + i_for_dc, 10)
            i_for_dc += 5
            nodelistDC.append(node)
            labels[node] = r'DC'
        if G.node[node].keys()[0] == 'POWERSTATION':
            pos[node] = (7 + i_for_power, 6)
            i_for_power += 6
            nodelistPower.append(node)
            labels[node] = r'P'
        if G.node[node].keys()[0] == 'INTERNET':
            pos[node] = (5 + i_for_internet, 2)
            i_for_internet += 5
            nodelistInternet.append(node)
            labels[node] = r'I'
        else:
            pass

    nx.draw_networkx_nodes(G, pos, nodelist = nodelistJob, \
            node_color = 'yellow', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodelistDC, \
            node_color = 'red', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodelistPower, \
            node_color = 'green', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodelistInternet, \
            node_color = 'blue', node_size = 400)
    #nx.draw(c1.topology)
    nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
    nx.draw_networkx_labels(G, pos, labels, font_size = 12)
    plt.show()  
    ''' 
