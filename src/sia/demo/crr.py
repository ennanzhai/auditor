
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
        
    def get_failure_of_datacenter(self, node):
        dcTopo = self.faultTree.node[node]['DATACENTER'].topology
        for item in dcTopo.node:
            if dcTopo.node[item].keys()[0] == 'ROUTER':
                dcTopo.node[item]['ROUTER'].stickyBit = 0
            if dcTopo.node[item].keys()[0] == 'AGGSWITCH':
                dcTopo.node[item]['AGGSWITCH'].stickyBit = 0
            if dcTopo.node[item].keys()[0] == 'RACK':
                dcTopo.node[item]['RACK'].stickyBit = 0

        # now we need to compute failure probability of datacenter
        result = 1
        routerPro = 1.0
        aggPro = 1.0
        switchPro = 1.0
        serverPro = 1.0
 
        # initialize a neighbor list
        neighborList = []
        cutSet = []
        subSet = []

        for item in dcTopo.node: 
            if dcTopo.node[item].keys()[0] == 'AGGSWITCH':
                subSet = []
                neighborList = dcTopo.neighbors(item)
               
                if dcTopo.node[item]['AGGSWITCH'].stickyBit == 1:
                    continue

                for i in range(0, len(neighborList)):
                    if neighborList[i] < item:
                        if dcTopo.node[neighborList[i]]['ROUTER']\
                                .stickyBit == 0:
                            dcTopo.node[neighborList[i]]['ROUTER'].happen \
                            = random_generator(dcTopo.node[neighborList[i]]\
                            ['ROUTER'].failure)
                            dcTopo.node[neighborList[i]]['ROUTER']\
                                    .stickyBit = 1

                        if dcTopo.node[neighborList[i]]['ROUTER']\
                                .happen == 0:
                            subSet = []  
                            break
                        else:
                            subSet.append(dcTopo\
                                    .node[neighborList[i]]['ROUTER'])
 
                tmpHappen = random_generator(dcTopo\
                        .node[item]['AGGSWITCH'].failure)
                
                if tmpHappen == 1:
                    dcTopo.node[item]['AGGSWITCH'].happen = 1
                    dcTopo.node[item]['AGGSWITCH'].cutSet\
                            .append(dcTopo.node[item]['AGGSWITCH'])
                elif subSet:
                    dcTopo.node[item]['AGGSWITCH'].happen = 1
                    dcTopo.node[item]['AGGSWITCH'].cutSet.extend(subSet)
                else:
                    dcTopo.node[item]['AGGSWITCH'].happen = 0
                dcTopo.node[item]['AGGSWITCH'].stickyBit = 1
                
        for item in dcTopo.node: 
            if dcTopo.node[item].keys()[0] == 'RACK':
                subSet = []
                neighborList = dcTopo.neighbors(item)
               
                if dcTopo.node[item]['RACK'].stickyBit == 1:
                    continue

                for i in range(0, len(neighborList)):
                    if neighborList[i] < item:
                        if dcTopo.node[neighborList[i]]['AGGSWITCH']\
                                .stickyBit == 0:
                            dcTopo.node[neighborList[i]]['AGGSWITCH']\
                                    .happen = random_generator(\
                                    dcTopo.node[neighborList[i]]\
                                    ['AGGSWITCH'].failure)
                            
                            dcTopo.node[neighborList[i]]['AGGSWITCH']\
                                    .stickyBit = 1

                        if dcTopo.node[neighborList[i]]['AGGSWITCH']\
                                .happen == 0:
                            subSet = []  
                            break
                        else:
                            subSet.append(dcTopo\
                                    .node[neighborList[i]]['AGGSWITCH'])
 
                tmpHappen = random_generator(dcTopo\
                        .node[item]['RACK'].failure)
                
                if tmpHappen == 1:
                    dcTopo.node[item]['RACK'].happen = 1
                    dcTopo.node[item]['RACK'].cutSet\
                            .append(dcTopo.node[item]['RACK'])
                elif subSet:
                    dcTopo.node[item]['RACK'].happen = 1
                    dcTopo.node[item]['RACK'].cutSet.extend(subSet)
                    self.finalMinimalCut.extend(subSet)
                else:
                    dcTopo.node[item]['RACK'].happen = 0
                    self.finalMinimalCut = []
                    result = 0
                    dcTopo.node[item]['RACK'].stickyBit = 1
                    break
                    
                dcTopo.node[item]['RACK'].stickyBit = 1

        '''
        # minimal cut sets need to refine
        # this step removes redundant items
        for i in range(0, len(self.finalMinimalCut)):
            tmpList = list(self.finalMinimalCut[i])
            for j in range(0, len(tmpList)):
                for k in range(j + 1, len(tmpList)):
                    if tmpList[j] == tmpList[k]:
                        if tmpList[j] in self.finalMinimalCut[i]:
                            self.finalMinimalCut[i].remove(tmpList[j])
        
        # enable all the cut sets to be the minimal
        baseList = list(self.finalMinimalCut)
        for i in range(0, len(baseList)):
            tmpListL = baseList[i]
            for j in range(i + 1, len(baseList)):
                tmpListR = baseList[j]
                if set(tmpListL).issubset(tmpListR):
                    if tmpListL in self.finalMinimalCut:
                        self.finalMinimalCut.remove(tmpListL)
                        continue
                if set(tmpListR).issubset(tmpListL):
                    if tmpListR in self.finalMinimalCut:
                        self.finalMinimalCut.remove(tmpListR)
        '''
        #print("----- Minimal Cut Sets -----")
        #print(self.finalMinimalCut)
        '''
        for i in range(0, len(self.finalMinimalCut)):
            print('The %d minimal cut set:'%(i+1))
            print("[")
            for j in range(0, len(self.finalMinimalCut[i])):
                print('%s : %d'%(self.finalMinimalCut[i][j].typeName,self.finalMinimalCut[i][j].ID))
            print("]")
            print(" ")

        self.faultTree.node[node]['DATACENTER'].cutSet \
                = self.finalMinimalCut
        '''
        #result = 0
        return result

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
                tmpHappen = random_generator(self\
                        .faultTree.node[node]['DATACENTER'].failure)
                    
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
