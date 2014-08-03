'''

This file mainly aims to define class for 
each component of datacenter:  
1) router
2) aggregation switch
3) access switch
4) rack
5) server

'''

from configuration import *
from hardware import *
import networkx as nx

# For each server, it must have:
# 1) ID and 
# 2) failure probability
class Rack: 
    def __init__(self, ID = 0):
        self.ID = ID
        self.hardware = Hardware('RACK')
        self.hardwareFailure = self.hardware.failure
        self.otherFailure = 0.0
        self.failure = self.hardwareFailure + self.otherFailure\
                       - self.hardwareFailure * self.otherFailure
        self.cutSet = []
        self.typeName = "Rack"
        self.happen = 0
        self.stickyBit = 0
    
# For each aggregation switch, it must have:
# 1) ID and 
# 2) failure probability       
class AggSwitch:
    def __init__(self, ID = 0):
        self.ID = ID
        self.hardware = Hardware('AGGSWITCH')
        self.hardwareFailure = self.hardware.failure
        self.otherFailure = 0.0
        self.failure = self.hardwareFailure + self.otherFailure\
                       - self.hardwareFailure * self.otherFailure
        self.cutSet = []
        self.typeName = "AggregationSwitch"
        self.happen = 0
        self.stickyBit = 0

# For each router, it must have:
# 1) ID and 
# 2) failure probability       
class Router:
    def __init__(self, ID = 0):
        self.ID = ID
        self.hardware = Hardware('ROUTER')
        self.hardwareFailure = self.hardware.failure
        self.otherFailure = 0.0
        self.failure = self.hardwareFailure + self.otherFailure\
                       - self.hardwareFailure * self.otherFailure
        self.cutSet =[]
        self.typeName = "Router"
        self.happen = 0
        self.stickyBit = 0
