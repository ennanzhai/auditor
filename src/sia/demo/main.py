'''
Main

'''

from cloudGenerator import *
from cloud import *
from hardware import *
from component import *
from datacenter import *
import matplotlib.pyplot as plt
import networkx as nx
from crr import *
from toolsforcrr import *

if __name__ == '__main__':
    '''
    c1 = Cloud(1, 1, 1, 2, 2)
    c2 = Cloud(2, 1, 1, 2, 2)
    cloudList = []
    cloudList.append(c1)
    cloudList.append(c2)
    
    s1 = SaaS(1)
    s2 = SaaS(1)
    saasList = []
    saasList.append(s1)
    saasList.append(s2)

    a1 = App(6)
    appList = []
    appList.append(a1)
    '''
    c = CloudGenerator()
    c.cloudGenerator(3, 3, 3)  # three cloud providers, two SaaSs and two Jobs

    # generating correlation
    # the first parameter is SaaS and the second one is cloud 
    matrix = []
    x = Correlation(base * 8 + 1, 1, 1)
    matrix.append(x)
    x = Correlation(base * 8 + 1, 2, 1)
    matrix.append(x)
    x = Correlation(base * 8 + 1, 3, 0)
    matrix.append(x)
    x = Correlation(base * 8 + 2, 1, 0)
    matrix.append(x)
    x = Correlation(base * 8 + 2, 2, 1)
    matrix.append(x)
    x = Correlation(base * 8 + 2, 3, 1)
    matrix.append(x)
    x = Correlation(base * 8 + 3, 1, 0)
    matrix.append(x)
    x = Correlation(base * 8 + 3, 2, 0)
    matrix.append(x)
    x = Correlation(base * 8 + 3, 3, 1)
    matrix.append(x)


    crr = CRR(c.cloudList, c.saasList, c.appList, matrix)

    crr.generateFaultTree()   
    
    change_failure_of_server(crr.faultTree, \
                             base * 7 + 1, \
                             base * 7 + 4, \
                             0.4)
    change_failure_of_server(crr.faultTree, \
                             base * 7 + 5, \
                             base * 7 + 8, \
                             0.2)
    change_failure_of_server(crr.faultTree, \
                             base * 7 + 9, \
                             base * 7 + 12, \
                             0.04)
    
    crr.compFailurePro()
    
    pos = {}
    i_for_server = 0.0
    i_for_switch = 0.0
    i_for_agg = 0.0
    i_for_router = 0.0
    i_for_service = 0.0
    i_for_vm = 0.0
    i_for_job = 0.0

    nodelist_for_server = []
    nodelist_for_switch = []
    nodelist_for_agg = []
    nodelist_for_router = []
    nodelist_for_service = []
    nodelist_for_vm = []
    nodelist_for_job = []

    labels = {}
    G = crr.faultTree

    provider1 = []
    provider2 = []
    provider3 = []

    for i in range(base * 2 + 1, dict_ID['ROUTER'] + 1):
        nodelist_for_router.append(i)
        pos[i] = (5 + i_for_router, 0.2)
        labels[i] = r'R'
        i_for_router += 50    
    for i in range(base * 3 + 1, dict_ID['AGGSWITCH'] + 1):
  	nodelist_for_agg.append(i)
	pos[i] = (5 + i_for_agg, 0.4)
	i_for_agg += 50
	labels[i] = r'Agg'
    for i in range(base * 4 + 1, dict_ID['RACK'] + 1):
	nodelist_for_switch.append(i)
	pos[i] = (5 + i_for_switch, 0.6)
	i_for_switch += 50
	labels[i] = r'SW'
    for i in range(base * 7 + 1, dict_ID['SERVER'] + 1):
	nodelist_for_server.append(i)
	pos[i] = (1 + i_for_server, 1.0)
	i_for_server += 20
	labels[i] = r'S'
    for i in range(base * 8 + 1, dict_ID['SERVICE'] + 1):
	nodelist_for_service.append(i)
	pos[i] = (40 + i_for_service, 1.2)
	i_for_service += 75
	labels[i] = r'SS'
    for i in range(base * 10 + 1, dict_ID['VM'] + 1):
	nodelist_for_vm.append(i)
	pos[i] = (5 + i_for_vm, 1.4)
	i_for_vm += 12
	labels[i] = r'VM'
    for i in range(base * 11 + 1, dict_ID['JOB'] + 1):
	nodelist_for_job.append(i)
	pos[i] = (30 + i_for_job, 1.6)
	i_for_job += 75
	labels[i] = r'Job'

    '''
    for node in G:        
	if G.node[node].keys()[0] == 'SERVER':
	    pos[node] = (1 + i_for_server, 1.0)
	    labels[node] = r'S'
            i_for_server += 20
            nodelist_for_server.append(node)
	elif G.node[node].keys()[0] == 'SWITCH':
	    pos[node] = (0.5 + i_for_switch, 0.6)
            i_for_switch += 30
            labels[node] = r'SW'
            nodelist_for_switch.append(node)
   	elif G.node[node].keys()[0] == 'AGGSWITCH':
	    pos[node] = (0.2 + i_for_agg, 0.4)
            i_for_agg += 30
            labels[node] = r'Agg'
            nodelist_for_agg.append(node)
  	elif G.node[node].keys()[0] == 'ROUTER':
	    pos[node] = (0.4 + i_for_router, 0.2)
	    labels[node] = r'R'
            i_for_router += 25
            nodelist_for_router.append(node)
    	elif G.node[node].keys()[0] == 'SERVICE':
	    pos[node] = (50 + i_for_service, 1.2)
	    i_for_service += 100
	    labels[node] = r'SS'
	    nodelist_for_service.append(node)
	elif G.node[node].keys()[0] == 'VM':
	    pos[node] = (5 + i_for_vm, 1.4)
	    i_for_vm += 12
	    labels[node] = r'VM'
	    nodelist_for_vm.append(node)
	elif G.node[node].keys()[0] == 'JOB':
	    pos[node] = (30 + i_for_job, 1.6)
	    i_for_job += 50
	    labels[node] = r'Job'
	    nodelist_for_job.append(node) 
   	else:
	    pass
    nodelist_for_server.sort()
    nodelist_for_switch.sort()
    nodelist_for_agg.sort()
    nodelist_for_router.sort()
    nodelist_for_service.sort()
    nodelist_for_vm.sort()
    nodelist_for_job.sort()
    '''
    
    #nx.draw(G, pos, node_color = colors, node_size = 200)
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
    provider1.append(nodelist_for_router[4])
    provider1.append(nodelist_for_router[5])
    provider1.append(nodelist_for_switch[4])
    provider1.append(nodelist_for_switch[5])
    provider1.append(nodelist_for_agg[4])
    provider1.append(nodelist_for_agg[5])
    provider1.append(nodelist_for_server[8])
    provider1.append(nodelist_for_server[9])
    provider1.append(nodelist_for_server[10])
    provider1.append(nodelist_for_server[11])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'blue', node_size = 400)

    provider1 = []
    provider1.append(nodelist_for_service[0])
    provider1.append(nodelist_for_vm[0])
    provider1.append(nodelist_for_vm[1])
    provider1.append(nodelist_for_vm[2])
    provider1.append(nodelist_for_vm[3])
    provider1.append(nodelist_for_vm[4])
    provider1.append(nodelist_for_vm[5])
    provider1.append(nodelist_for_job[0])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'red', node_size = 500)
    provider1 = []
    provider1.append(nodelist_for_service[1])
    provider1.append(nodelist_for_vm[6])
    provider1.append(nodelist_for_vm[7])
    provider1.append(nodelist_for_vm[8])
    provider1.append(nodelist_for_vm[9])
    provider1.append(nodelist_for_vm[10])
    provider1.append(nodelist_for_vm[11])
    provider1.append(nodelist_for_job[1])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'orange', node_size = 500)
    provider1 = []
    provider1.append(nodelist_for_service[2])
    provider1.append(nodelist_for_vm[13])
    provider1.append(nodelist_for_vm[14])
    provider1.append(nodelist_for_vm[15])
    provider1.append(nodelist_for_vm[16])
    provider1.append(nodelist_for_vm[17])
    provider1.append(nodelist_for_vm[12])
    provider1.append(nodelist_for_job[2])
    nx.draw_networkx_nodes(G, pos, nodelist = provider1, \
            node_color = 'white', node_size = 500)

    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_agg,\
    #        node_color = 'white', node_size = 500)
    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_switch, \
    #        node_color = 'orange', node_size = 400)
    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_server, \
    #        node_color = 'red', node_size = 400)
    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_service, \
    #        node_color = 'green', node_size = 400)
    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_vm,\
    #        node_color = 'blue', node_size = 400)
    #nx.draw_networkx_nodes(G, pos, nodelist = nodelist_for_job, \
    #        node_color = 'green', node_size = 500)
    nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
    nx.draw_networkx_labels(G, pos, labels, font_size = 13)

    plt.show()  
