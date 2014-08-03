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
from crr import *
from job import *

if __name__ == '__main__':
    # 1
    start = time.clock()

    # 1 data center
    # 2 core routers
    # 2 agg switches
    # 4 racks
    c1 = Cloud(1, 4, 4, 4, 2, 2, 2, 2)

    # 2
    cloudList_for_job1 = []
    cloudList_for_job1.append(c1)
    typeCom = "RACK"

    # 3
    #
    app1 = App(1, 4, typeCom, cloudList_for_job1)
    appList = []
    appList.append(app1)

    # 4
    cloudList = []
    cloudList.append(c1)

    # 5
    crr = CRR(cloudList, appList)
    crr.build_fault_tree_for_app("Minimal")
    #crr.get_failure_of_app()
    
    end = time.clock()
    print(end - start)
    
    # 6

    G = nx.Graph()
    pos = { }
    labels={}
    G = crr.faultTree

    i_for_rack = 0.0
    i_for_router = 0.0
    i_for_agg = 0.0
    i_for_piece = 0.0
    i_for_app = 0.0

    nodeListRack = []
    nodeListRouter = []
    nodeListPiece = []
    nodeListAgg = []
    nodeListApp = []

    #print(G.node)

    for node in G:
        if G.node[node].keys()[0] == 'ROUTER':
            nodeListRouter.append(node)
            pos[node] = (5 + i_for_router, 0.2)
            labels[node] = r'R'
            i_for_router += 30
        if G.node[node].keys()[0] == 'AGGSWITCH':
            nodeListAgg.append(node)
            pos[node] = (10 + i_for_agg, 0.4)
            labels[node] = r'Agg'
            i_for_agg += 20
        if G.node[node].keys()[0] == 'RACK':
            nodeListRack.append(node)
            pos[node] = (13 + i_for_rack, 0.6)
            labels[node] = r'RA'
            i_for_rack += 14
        if G.node[node].keys()[0] == 'PIECE':
            nodeListPiece.append(node)
            pos[node] = (13 + i_for_piece, 0.8)
            labels[node] = r'P'
            i_for_piece += 14
        if G.node[node].keys()[0] == 'JOB':
            nodeListApp.append(node)
            pos[node] = (20 + i_for_app, 1.0)
            labels[node] = r'JOB'
            i_for_app += 30

    nx.draw_networkx_nodes(G, pos, nodelist = nodeListRouter,\
           node_color = 'yellow', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodeListAgg,\
           node_color = 'orange', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodeListRack,\
           node_color = 'green', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodeListPiece,\
           node_color = 'green', node_size = 400)
    nx.draw_networkx_nodes(G, pos, nodelist = nodeListApp,\
           node_color = 'yellow', node_size = 400)
    nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
    nx.draw_networkx_labels(G, pos, labels, font_size = 12)
    
    plt.show()  
