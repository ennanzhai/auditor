
import copy
from random import *
from cloud import *
import networkx as nx
from mathheader import *
from identity import *

class CRR:
    def __init__(self, cloudList, appList):
        self.cloudList = []
	self.appList = []        
        
        self.faultTree = nx.Graph()
	self.faultTreeDraw = nx.Graph()

        self.cloudList = cloudList
	self.appList = appList

        self.cloudNum = len(self.cloudList)
        self.appNum = len(self.appList)

        self.minimal_cut = []
        self.finalMinimalCut = []

    def build_fault_tree_for_app(self):
        recordCloudList = []
        nonOverlapping = 1
        for cloudItem in self.cloudList:    
            if self.faultTree.number_of_nodes() == 0:
                self.faultTree = cloudItem.topology
            else:
                for i in range(len(cloudItem.dataCenterID)):
                    if cloudItem.dataCenterID[i] in recordCloudList:
                        nonOverlapping = 0
                        break                
                if nonOverlapping == 1:
                    self.faultTree \
                            = nx.union(self.faultTree, cloudItem.topology)
            for i in range(len(cloudItem.dataCenterID)):
                recordCloudList.append(cloudItem.dataCenterID[i])
        
        for appItem in self.appList:
            self.faultTree = nx.union(self.faultTree, appItem.topology)
            for dcItem in self.faultTree.node:
                if self.faultTree.node[dcItem].keys()[0] == 'DATACENTER'\
                        and dcItem in appItem.dcList:
                    self.faultTree.add_edge(dcItem, appItem.jobID)
    
    def get_failure_of_app(self):
        neighborList = []
        finalResult = 1.0
        finalResult = 1.0
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'DATACENTER':
                powerFailure = 1.0
                routerFailure = 1.0

                neighborList = self.faultTree.neighbors(node)
                powerList = []
                InternetList = [] 
                
                powerFailure = 1.0
                routerFailure = 1.0
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= powerBase \
                            and neighborList[i] < InternetBase:
                        #powerFailure *= self.faultTree\
                        #    .node[neighborList[i]]['POWERSTATION'].failure
                        if powerFailure > self.faultTree.node[neighborList[i]]['POWERSTATION'].failure:
                            powerFailure = self.faultTree.node[neighborList[i]]['POWERSTATION'].failure
                    if neighborList[i] >= InternetBase \
                            and neighborList[i] < dcBase:
                        #routerFailure *= self.faultTree\
                        #    .node[neighborList[i]]['INTERNET'].failure
                        if routerFailure > self.faultTree.node[neighborList[i]]['INTERNET'].failure:
                            routerFailure = self.faultTree.node[neighborList[i]]['INTERNET'].failure
                self.faultTree.node[node]['DATACENTER'].failure \
                         = 0.047723 + powerFailure + routerFailure
                #        = 1-(1-0.047723)*(1-powerFailure)*(1-routerFailure)
                print(self.faultTree.node[node]['DATACENTER'].failure)

                #finalResult *= self.faultTree.node[node]['DATACENTER'].failure
                if finalResult > self.faultTree.node[node]['DATACENTER'].failure:
                    finalResult = self.faultTree.node[node]['DATACENTER'].failure
        print(finalResult)
                
                
