'''
This file mainly aims to generate datacenter
'''

import networkx as nx
import matplotlib.pyplot as plt
import random
from component import *
from identity import *

class DataCenter:
    '''
    classdocs
    '''
    def __init__(self, routerNum = DEFAULT_ROUTER_NUM_IN_A_DC, \
                       aggSwitchNum = DEFAULT_AGGSWITCH_NUM_IN_A_DC, \
                       rackNum = DEFAULT_RACK_NUM_IN_A_DC, \
                       serverNum = DEFAULT_SERVER_NUM_IN_A_RACK, \
                       powerNum = DEFAULT_POWER_NUM_IN_A_DC):  
        
        # initialize vectors for components
        self.topology = nx.Graph()
        self.routerID = []
        self.aggSwitchID = []
        self.rackID = []
        self.powerID = []
        
        # initialize numbers for components
        self.routerNum = routerNum
        self.aggSwitchNum = aggSwitchNum
        self.rackNum = rackNum
        self.powerNum = powerNum
        
	# initialize each router and add them into the graph
        recordRouter = dict_ID['ROUTER'] + 1
	for i in range(self.routerNum):
            tmpID = dict_ID['ROUTER'] + 1  # extract the newest router ID
            self.routerID.append(tmpID)    # append the ID
            dict_ID['ROUTER'] = tmpID      # ID++
            self.topology.add_node(tmpID)  # the index of the new node
            self.topology.node[tmpID]['ROUTER'] = Router(tmpID)
        
	# initialize each aggSwitch and add them into the graph
        recordAggswitch = dict_ID['AGGSWITCH'] + 1
        for i in range(self.aggSwitchNum):
            tmpID = dict_ID['AGGSWITCH'] + 1  # extract the newest agg ID
            self.aggSwitchID.append(tmpID)    # append the ID
            dict_ID['AGGSWITCH'] = tmpID      # ID++
            self.topology.add_node(tmpID)
            self.topology.node[tmpID]['AGGSWITCH'] = AggSwitch(tmpID)
        
	# initialize each rack and add them into the graph
        recordRack = dict_ID['RACK'] + 1
	for i in range(self.rackNum):
            tmpID = dict_ID['RACK'] + 1
            self.rackID.append(tmpID)
            dict_ID['RACK'] = tmpID
	    self.topology.add_node(tmpID)
	    self.topology.node[tmpID]['RACK'] = Rack(serverNum)
	    self.topology.node[tmpID]['RACK'].ID = tmpID
        
        # initialize each power station and add them into the graph
        recordPower = dict_ID['POWERSTATION'] + 1
        for i in range(self.powerNum):
            tmpID = dict_ID['POWERSTATION'] + 1
            self.powerID.append(tmpID)
            dict_ID['POWERSTATION'] = tmpID
            self.topology.add_node(tmpID)
            self.topology.node[tmpID]['POWERSTATION'] = PowerStation(tmpID)

	'''
        Generate the edges
        '''
        #Add the connected components information of router and aggSwitch
        for routerIndex in range(recordRouter, dict_ID['ROUTER'] + 1):
            for aggIndex in range(recordAggswitch, \
                                  dict_ID['AGGSWITCH'] + 1):
                self.topology.add_edge(routerIndex, aggIndex)
                    
	for rackIndex in range(recordRack, dict_ID['RACK'] + 1):
            randAggSwitch = random.randint(recordAggswitch, \
                                           dict_ID['AGGSWITCH'])
            self.topology.add_edge(rackIndex, randAggSwitch)
	    if randAggSwitch == dict_ID['AGGSWITCH']:
		self.topology.add_edge(rackIndex, recordAggswitch)
            else:
		self.topology.add_edge(rackIndex, randAggSwitch + 1)
        
        for powerIndex in range(recordPower, dict_ID['POWERSTATION'] + 1):
            for routerIndex in range(recordRouter, dict_ID['ROUTER'] + 1):
                self.topology.add_edge(powerIndex, routerIndex)
            for aggIndex in range(recordAggswitch, \
                    dict_ID['AGGSWITCH'] + 1):
                self.topology.add_edge(powerIndex, aggIndex)
            for rackIndex in range(recordRack, dict_ID['RACK'] + 1):
                self.topology.add_edge(powerIndex, rackIndex)
                
