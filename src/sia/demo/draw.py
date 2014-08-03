'''

This file is used to draw

'''

import matplotlib.pyplot as plt
import networkx as nx
from identity import *


def draw(faultTree):
    pos = {}

    i_for_server = 0.0
    i_for_switch = 0.0
    i_for_agg = 0.0
    i_for_router = 0.0
    i_for_vm = 0.0
    i_for_job = 0.0

    nodelist_for_server = []
    nodelist_for_switch = []
    nodelist_for_agg = []
    nodelist_for_router = []
    nodelist_for_vm = []
    nodelist_for_job = []

    labels = {}
    G = faultTree
    provider1 = []

    for i in range(base * 2 + 1, dict_ID['ROUTER'] + 1):
        nodelist_for_router.append(i)
        pos[i] = (5 + i_for_router, 0.2)
        labels[i] = r'R'
        i_for_router += 50    
    for i in range(base * 3 + 1, dict_ID['AGGSWITCH'] + 1):
  	nodelist_for_agg.append(i)
	pos[i] = (5 + i_for_agg, 0.4)
	i_for_agg += 50
        labels[i] = r'A'
    for i in range(base * 4 + 1, dict_ID['RACK'] + 1):
	nodelist_for_switch.append(i)
	pos[i] = (5 + i_for_switch, 0.6)
	i_for_switch += 50
	labels[i] = r'SW'
    for i in range(base * 7 + 1, dict_ID['SERVER'] + 1):
	nodelist_for_server.append(i)
	pos[i] = (1 + i_for_server, 1.0)
	i_for_server += 22
	labels[i] = r'S'
    for i in range(base * 10 + 1, dict_ID['VM'] + 1):
	nodelist_for_vm.append(i)
	pos[i] = (40 + i_for_vm, 1.4)
	i_for_vm += 70
	labels[i] = r'VM'
    for i in range(base * 11 + 1, dict_ID['JOB'] + 1):
	nodelist_for_job.append(i)
	pos[i] = (75 + i_for_job, 1.6)
	i_for_job += 75
	labels[i] = r'Job'
    

    provider1.append(nodelist_for_router[0])
    provider1.append(nodelist_for_router[1])
    provider1.append(nodelist_for_switch[0])
    provider1.append(nodelist_for_switch[1])
    provider1.append(nodelist_for_agg[0])
    provider1.append(nodelist_for_agg[1])
    provider1.append(nodelist_for_server[0])
    provider1.append(nodelist_for_server[1])
    provider1.append(nodelist_for_server[2])
    provider1.append(nodelist_for_server[3])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'yellow', node_size = 400)

    provider1 = []
    provider1.append(nodelist_for_router[2])
    provider1.append(nodelist_for_router[3])
    provider1.append(nodelist_for_switch[2])
    provider1.append(nodelist_for_switch[3])
    provider1.append(nodelist_for_agg[2])
    provider1.append(nodelist_for_agg[3])
    provider1.append(nodelist_for_server[4])
    provider1.append(nodelist_for_server[5])
    provider1.append(nodelist_for_server[6])
    provider1.append(nodelist_for_server[7])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'green', node_size = 400)

    provider1 = []
    provider1.append(nodelist_for_vm[0])
    provider1.append(nodelist_for_vm[1])
    provider1.append(nodelist_for_job[0])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'red', node_size = 500)
    nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
    nx.draw_networkx_labels(G, pos, labels, font_size = 13)

    plt.show()  
