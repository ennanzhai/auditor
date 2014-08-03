
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
                dcTopo.node[item]['ROUTER'].happen = 0
            if dcTopo.node[item].keys()[0] == 'AGGSWITCH':
                dcTopo.node[item]['AGGSWITCH'].stickyBit = 0
                dcTopo.node[item]['AGGSWITCH'].happen = 0
            if dcTopo.node[item].keys()[0] == 'RACK':
                dcTopo.node[item]['RACK'].stickyBit = 0
                dcTopo.node[item]['RACK'].happen = 0

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
                if subSet:
                    dcTopo.node[item]['AGGSWITCH'].happen = 1
                    dcTopo.node[item]['AGGSWITCH'].cutSet.extend(subSet)
                #else:
                #    dcTopo.node[item]['AGGSWITCH'].happen = 0
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
                if subSet:
                    dcTopo.node[item]['RACK'].happen = 1
                    dcTopo.node[item]['RACK'].cutSet.extend(subSet)
                    self.finalMinimalCut.extend(subSet)
                
                if dcTopo.node[item]['RACK'].happen == 0:
                    dcTopo.node[item]['RACK'].happen = 0
                    self.finalMinimalCut = []
                    result = 0
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
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'DATACENTER':
                neighborList = self.faultTree.neighbors(node)
                powerList = []
                InternetList = [] 
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= powerBase \
                            and neighborList[i] < InternetBase:
                        powerList.append(\
                            self.faultTree\
                            .node[neighborList[i]]['POWERSTATION'])
                    if neighborList[i] >= InternetBase \
                            and neighborList[i] < dcBase:
                        InternetList.append(\
                            self.faultTree\
                            .node[neighborList[i]]['INTERNET'])
                self.faultTree.node[node]['DATACENTER'].powerCutSet\
                        = list(powerList)
                self.faultTree.node[node]['DATACENTER'].InternetCutSet\
                        = list(InternetList)
                
                # get failure probability

                self.faultTree.node[node]['DATACENTER'].failure = 0.01
                counter = 0.0
                
                for count in range(0, 10000):
                    isHappen = self.get_failure_of_datacenter(node)
                    if isHappen == 1:
                        counter += 1.0
                print('------------ result: %f'%(counter/10000.0))
                
                self.faultTree.node[node]['DATACENTER'].cutSet = []
                subSet = []
                subSet.append(self.faultTree.node[node]['DATACENTER'])
                self.faultTree.node[node]['DATACENTER']\
                        .cutSet.append(subSet)
                
                self.faultTree.node[node]['DATACENTER']\
                        .cutSet.append(self.faultTree\
                        .node[node]['DATACENTER'].powerCutSet)
                
                self.faultTree.node[node]['DATACENTER'].cutSet\
                        .append(self.faultTree.node[node]['DATACENTER']\
                        .InternetCutSet)
                
                if not appResult:
                    appResult = list(self.faultTree\
                            .node[node]['DATACENTER'].cutSet)
                else:
                    keepSet = list(appResult)
                    for i in range(0, len(keepSet)):
                        for j in range(0, len(self.faultTree\
                                .node[node]['DATACENTER'].cutSet)):
                            tmp = list(keepSet[i])
                            tmp.extend(self.faultTree\
                                    .node[node]['DATACENTER'].cutSet[j])
                            appResult.append(tmp)
                            if keepSet[i] in appResult:
                                appResult.remove(keepSet[i])

        # minimal cut sets need to refine
        tmpList = []
        for i in range(0, len(appResult)):
            tmpList = list(appResult[i])
            for j in range(0, len(tmpList)):
                for k in range(j+1, len(tmpList)):
                    if tmpList[j] == tmpList[k]:
                        if appResult[i].count(tmpList[j]) > 1:
                            appResult[i].remove(tmpList[j])
        
        # enable all the cut sets to be the minimal
        baseList = list(appResult)
        for i in range(0, len(baseList)):
            tmpListL = baseList[i]
            #print(baseList[i])
            for j in range(i+1, len(baseList)):
                if j >= len(baseList):
                    break
                tmpListR = baseList[j]
                if set(tmpListL).issubset(tmpListR):
                    if tmpListL in appResult:
                        appResult.remove(tmpListL)
                elif set(tmpListR).issubset(tmpListL):
                    if tmpListR in appResult:
                        appResult.remove(tmpListR)
                else:
                    pass
            #print(len(appResult))
        
        print("----- Minimal Cut Sets -----")
        resultList = []
        for i in range(0, len(appResult)):
            resultList.append(1.0)
        for i in range(0, len(appResult)):
            print('The %d minimal cut set:'%(i+1))
            print("[")
            for j in range(0, len(appResult[i])):
                print('%s : %d, failure: %f'%(appResult[i][j].typeName,\
                        appResult[i][j].ID,\
                        appResult[i][j].failure))
                resultList[i] *= appResult[i][j].failure
            print("]")
            print('The failure probability of this cut set is: %f'\
                    %(resultList[i]))
            print("===============")

        # Let us present importance
        tmpResult = 1.0
        for i in range(0, len(resultList)):
            tmpResult *= (1 - resultList[i])
        result = 1 - tmpResult
        print('The failure probability of application is %f'%(result))
        importance = []
        for i in range(0, len(resultList)):
            importance.append(resultList[i]/result)
            print('The importance of Cut Set %d is: %f'\
                    %((i+1), importance[i]))

    '''
def combine(cloud1, cloud2):
    c = Cloud(0, 0, 0, 0, 0)
    c.topology = nx.Graph()
    c.dataCenterID = []
    c.dcNum = cloud1.dcNum + cloud2.dcNum
    c.dataCenterID = cloud1.dataCenterID + cloud2.dataCenterID
    c.topology = nx.union(cloud1.topology, cloud2.topology)
    return c
    '''

