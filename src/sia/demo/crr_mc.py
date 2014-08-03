
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
        self.finalMinimalCut = []
        appResult = []
        result = 1

        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'DATACENTER':
                self.faultTree.node[node]['DATACENTER'].stickyBit = 0
                self.faultTree.node[node]['DATACENTER'].happen = 0
            if self.faultTree.node[node].keys()[0] == 'POWERSTATION':
                self.faultTree.node[node]['POWERSTATION'].stickyBit = 0
                self.faultTree.node[node]['POWERSTATION'].happen = 0
            if self.faultTree.node[node].keys()[0] == 'INTERNET':
                self.faultTree.node[node]['INTERNET'].stickyBit = 0
                self.faultTree.node[node]['INTERNET'].happen = 0
        
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'DATACENTER':
                neighborList = self.faultTree.neighbors(node)
                powerList = []
                InternetList = [] 
                if self.faultTree.node[node]['DATACENTER'].stickyBit == 1:
                    continue

                for i in range(0, len(neighborList)):
                    if neighborList[i] >= powerBase \
                            and neighborList[i] < InternetBase:
                        if self.faultTree\
                                .node[neighborList[i]]['POWERSTATION']\
                                .stickyBit == 0:
                            self.faultTree\
                            .node[neighborList[i]]['POWERSTATION'].happen\
                            = random_generator(self.faultTree\
                            .node[neighborList[i]]['POWERSTATION'].failure)

                            self.faultTree.node[neighborList[i]]\
                                    ['POWERSTATION'].stickyBit = 1
                        
                        if self.faultTree.node[neighborList[i]]\
                                ['POWERSTATION'].happen == 0:
                            powerList = []
                            break
                        else:
                            powerList.append(self.faultTree\
                                .node[neighborList[i]]['POWERSTATION'])

                for i in range(0, len(neighborList)):
                    if neighborList[i] >= InternetBase \
                            and neighborList[i] < dcBase:
                        if self.faultTree\
                                .node[neighborList[i]]['INTERNET']\
                                .stickyBit == 0:
                            self.faultTree\
                            .node[neighborList[i]]['INTERNET'].happen\
                            = random_generator(self.faultTree\
                            .node[neighborList[i]]['INTERNET'].failure)

                            self.faultTree.node[neighborList[i]]\
                                    ['INTERNET'].stickyBit = 1
                        
                        if self.faultTree.node[neighborList[i]]\
                                ['INTERNET'].happen == 0:
                            InternetList = []
                            break
                        else:
                            InternetList.append(self.faultTree\
                                .node[neighborList[i]]['INTERNET'])

                #tmpHappen = random_generator(0.05)
                tmpHappen = random_generator(0.047723)
                    
                if tmpHappen == 1:
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER'].cutSet\
                        .append(self.faultTree.node[node]['DATACENTER'])
                if powerList:
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER']\
                            .cutSet.extend(powerList)
                if InternetList:
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER']\
                            .cutSet.extend(InternetList)
                 
                if self.faultTree.node[node]['DATACENTER'].happen == 0:
                    result = 0
                    return 0
                    
                self.faultTree.node[node]['DATACENTER'].stickyBit = 1
                                 
                #self.faultTree.node[node]['DATACENTER'].stickyBit = 1

        return result                
