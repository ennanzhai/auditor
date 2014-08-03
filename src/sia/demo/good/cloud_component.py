'''

This file mainly aims to generate three components for cloud:
1) power station
2) Internet provider
3) datacenter

'''

import networkx as nx
from datacenter_component import *
import random

# For each power station, it must have:
# 1) ID and 
# 2) failure probability
class PowerStation:
    def __init__(self, ID = 0):
        self.ID = ID
        self.failure = DEFAULT_FAILURE_OF_POWERSTATION
        self.typeName = "Power Station"
        self.happen = 0
        self.stickyBit = 0

# For each Internet provider, it must have:
# 1) ID and
# 2) failure probability
class InternetProvider:
    def __init__(self, ID = 0):
        self.ID = ID
        self.failure = DEFAULT_FAILURE_OF_INTERNET
        self.typeName = "Internet Routers"
        self.happen = 0
        self.stickyBit = 0

# For each datacenter, it must have:
# 1) ID,
# 2) router list, router number
# 3) aggregation switch list, aggregation switch number
# 4) rack list, rack number
# 5) topology
# 6) failure probability
class DataCenter:
    def __init__(self, \
                 routerNum = DEFAULT_ROUTER_NUM_IN_A_DC, \
                 aggSwitchNum = DEFAULT_AGGSWITCH_NUM_IN_A_DC, \
                 rackNum = DEFAULT_RACK_NUM_IN_A_DC):  
        
        # initialize vectors for components
        self.topology = nx.Graph()
        self.routerID = []
        self.aggSwitchID = []
        self.rackID = []
        self.ID = 0  # this will be assigned by cloud
        self.failure = DEFAULT_FAILURE_OF_DC
        self.cutSet = []
        self.powerCutSet = []
        self.InternetCutSet = []
        self.happen = 0
        self.stickyBit = 0

        # initialize numbers for components
        self.routerNum = routerNum
        self.aggSwitchNum = aggSwitchNum
        self.rackNum = rackNum
        self.typeName = "Data Center"

	# initialize each router and add them into the graph
        recordRouter = dict_ID['ROUTER'] + 1
	for i in range(self.routerNum):
            dict_ID['ROUTER'] += 1 
            tmpID = dict_ID['ROUTER']      
            self.routerID.append(tmpID)    
            self.topology.add_node(tmpID)  
            self.topology.node[tmpID]['ROUTER'] = Router(tmpID)
        
	# initialize each aggSwitch and add them into the graph
        recordAggswitch = dict_ID['AGGSWITCH'] + 1
        for i in range(self.aggSwitchNum):
            dict_ID['AGGSWITCH'] += 1  
            tmpID = dict_ID['AGGSWITCH']
            self.aggSwitchID.append(tmpID)
            self.topology.add_node(tmpID)
            self.topology.node[tmpID]['AGGSWITCH'] = AggSwitch(tmpID)
        
	# initialize each rack and add them into the graph
        recordRack = dict_ID['RACK'] + 1
	for i in range(self.rackNum):
            dict_ID['RACK'] += 1
            tmpID = dict_ID['RACK']
            self.rackID.append(tmpID)
	    self.topology.add_node(tmpID)
	    self.topology.node[tmpID]['RACK'] = Rack(tmpID)
	
        # Generate the edges
        # Add the connected components information of router and aggSwitch
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
        
