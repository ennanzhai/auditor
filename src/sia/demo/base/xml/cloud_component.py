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
    def __init__(self, ID = 0, failure = DEFAULT_FAILURE_OF_POWERSTATION):
        self.ID = ID
        self.failure = failure
        self.typeName = "Power Supply"
        self.happen = 0
        self.stickyBit = 0

# For each Internet provider, it must have:
# 1) ID and
# 2) failure probability
class InternetProvider:
    def __init__(self, ID = 0, failure = DEFAULT_FAILURE_OF_INTERNET):
        self.ID = ID
        self.failure = DEFAULT_FAILURE_OF_INTERNET
        self.typeName = "Internet Router"
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
    def __init__(self, ID = 0, failure = DEFAULT_FAILURE_OF_DC):
                 
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

        self.typeName = "Data Center"

	
