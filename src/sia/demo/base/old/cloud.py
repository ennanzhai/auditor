'''

This file aims to generate cloud class

'''

import networkx as nx
import random
from cloud_component import *

class Cloud:
    '''
    For each cloud, it has: 1) dcNum (# of datacenter), 2) dataCenterID
    (an array of datacenter's IDs), 3) ID (cloud's ID), 4) inet_fail_prob
    (the failure probability of the Internet), and 5) topology
    '''
    def __init__(self, \
                 typeCloud, \
                 dcNum = DEFAULT_DC_NUM_IN_A_CLOUD, \
                 routerNum = DEFAULT_ROUTER_NUM_IN_A_DC,\
                 aggSwitchNum = DEFAULT_AGGSWITCH_NUM_IN_A_DC,\
                 rackNum = DEFAULT_RACK_NUM_IN_A_DC,\
                 powerNum = DEFAULT_POWER_NUM_IN_A_CLOUD,\
                 powerNumforEachDC = DEFAULT_POWER_NUM_FOR_A_DC,\
                 InternetNum = DEFAULT_INTERNET_NUM_IN_A_CLOUD,\
                 InternetNumforEachDC = DEFAULT_INTERNET_NUM_FOR_A_DC):
        
        self.topology = nx.Graph()

	# network consisting of data centers, power and Internet
        # We have datacenter list
        self.dcNum = dcNum
        self.dataCenterID = []

        # We have power station list
        self.powerNum = powerNum
        self.powerID = []

        # We have Internet provider list
        self.InternetNum = InternetNum
        self.InternetID = []

        # Initialize this cloud's ID
	dict_ID['CLOUD'] += 1
        self.ID = dict_ID['CLOUD']

        if typeCloud == "CORRELATION":
            # generate power stations in this cloud
            recordPower = dict_ID['POWERSTATION'] + 1
            for i in range(self.powerNum):
                dict_ID['POWERSTATION'] += 1
                tmpID = dict_ID['POWERSTATION']
                self.powerID.append(tmpID)
                self.topology.add_node(tmpID)
                self.topology.node[tmpID]['POWERSTATION'] \
                        = PowerStation(tmpID)

            # generate Internet providers in this cloud
            recordInternet = dict_ID['INTERNET'] + 1
            for i in range(self.InternetNum):
                dict_ID['INTERNET'] += 1
                tmpID = dict_ID['INTERNET']
                self.InternetID.append(tmpID)
                self.topology.add_node(tmpID)
                self.topology.node[tmpID]['INTERNET'] \
                        = InternetProvider(tmpID)
        
            # generate datacenters in the Cloud
            recordDC = dict_ID['DATACENTER'] + 1
            for i in range(self.dcNum): 
                dict_ID['DATACENTER'] += 1
                tmpID = dict_ID['DATACENTER']            
                self.dataCenterID.append(tmpID)  # fill out datacenterID
                self.topology.add_node(tmpID)

                self.topology.node[tmpID]['DATACENTER'] \
                    = DataCenter(routerNum, aggSwitchNum, rackNum)
                self.topology.node[tmpID]['DATACENTER'].ID = tmpID
	    
                #for j in range(recordDC, tmpID):
	        #	self.topology.add_edge(j, tmpID)
                # connect power stations and the current datacenter
                r = random.randint(1, powerNum)
                index = recordPower + (r % powerNum)
            
                for j in range(powerNumforEachDC):
                    self.topology.add_edge(index, tmpID)
                    r += 1
                    index = recordPower + (r % powerNum)
            
                # connect Internet providers and the current datacenter
                r = random.randint(1, InternetNum)
                index = recordInternet + (r % InternetNum)
                for j in range(InternetNumforEachDC):
                    self.topology.add_edge(index, tmpID)
                    r += 1
                    index = recordInternet + (r % InternetNum)
        else:
            for i in range(self.dcNum): 
                dict_ID['DATACENTER'] += 1
                tmpID = dict_ID['DATACENTER']            
                self.dataCenterID.append(tmpID)  # fill out datacenterID
                self.topology.add_node(tmpID)
                self.topology.node[tmpID]['DATACENTER'] \
                    = DataCenter(routerNum, aggSwitchNum, rackNum)
                self.topology.node[tmpID]['DATACENTER'].ID = tmpID
            
                for j in range(powerNumforEachDC):
                    dict_ID['POWERSTATION'] += 1
                    tmpPowerID = dict_ID['POWERSTATION']
                    self.powerID.append(tmpPowerID)
                    self.topology.add_node(tmpPowerID)
                    self.topology.node[tmpPowerID]['POWERSTATION'] \
                        = PowerStation(tmpPowerID)
                    self.topology.add_edge(tmpPowerID, tmpID)
                
                # connect Internet providers and the current datacenter
                for j in range(InternetNumforEachDC):
                    dict_ID['INTERNET'] += 1
                    tmpRouterID = dict_ID['INTERNET']
                    self.InternetID.append(tmpRouterID)
                    self.topology.add_node(tmpRouterID)
                    self.topology.node[tmpRouterID]['INTERNET'] \
                        = InternetProvider(tmpRouterID)
                    self.topology.add_edge(tmpRouterID, tmpID)


    def clone(self):
        c = Cloud(0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        c.topology = nx.Graph()
        c.topology = self.topology
        
        c.dataCenterID = []
        c.dcNum = self.dcNum
        c.dataCenterID = self.dataCenterID
        
        c.powerNum = self.powerNum
        c.powerID = self.powerID
        
        c.InternetNum = self.InternetNum
        c.InternetID = self.InternetID

        return c

