'''
Main

'''

from random import random
from cloud import *
import matplotlib.pyplot as plt
import networkx as nx
from crr import *

if __name__ == '__main__':
    
    #c1 = Cloud(1, 2, 2, 2, 5, 5, 2, 2, 1)
    dc = DataCenter(4, 4, 5, 5)
    
    colors = ['red', 'blue', 'yellow']
    G = dc.topology

    pos = { }

    i_for_rack = 0.0
    i_for_switch = 0.0
    i_for_agg = 0.0
    i_for_router = 0.0

    nodelistRack = []
    nodelistSwitch = []
    nodelistAgg = []
    nodelistRouter = []
    
    for node in G:
        if G.node[node].keys()[0] == 'RACK':
            pos[node] = (0.1 + i_for_rack, 1.0)
            i_for_rack += 3.5
            nodelistRack.append(node)
        elif G.node[node].keys()[0] == 'SWITCH':
            pos[node] = (0.5 + i_for_switch, 0.6)
            i_for_switch += 7.5
            nodelistSwitch.append(node)
        elif G.node[node].keys()[0] == 'AGGSWITCH':
            pos[node] = (0.2 + i_for_agg, 0.4)
            i_for_agg += 4.0
            nodelistAgg.append(node)
        elif G.node[node].keys()[0] == 'ROUTER':
            pos[node] = (0.4 + i_for_router, 0.2)
            i_for_router += 5.0
            nodelistRouter.append(node)
        else:
            pass

    nx.draw(G, pos, node_color = colors, node_size = 300)
    nx.draw(G, pos, node_color = colors, node_size = 300)
    nx.draw(G, pos, node_color = colors, node_size = 300)
    nx.draw(G, pos, node_color = colors, node_size = 300)
    
    plt.show()  
