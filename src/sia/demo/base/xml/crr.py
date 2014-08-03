
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

    def build_fault_tree_for_app(self, algorithm):
        recordCloudList = []
        # At the beginning, there is no overlapping
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
            if appItem.appType == "DATACENTER":
                self.faultTree = nx.union(self.faultTree, appItem.topology)
                for i in range(len(appItem.pieceID)):
                    choiceList = random.sample(appItem.dcList, \
                                               appItem.replicaNum)
                    for j in range(appItem.replicaNum):
                        self.faultTree.add_edge(appItem.pieceID[i], \
                                choiceList[j])
                if algorithm == "MC":
                    # begin computing failures
                    counter = 0.0
                    for i in range(0, TRIALS):
                        isHappen = self.get_failure_of_app_via_mc()
                        if isHappen == 1:
                            counter += 1.0
                    print(counter/float(TRIALS))
                elif algorithm == "Min":
                    self.get_failure_of_app_via_mcs()
                elif algorithm == "Naive":
                    self.get_failure_of_app_via_naive()
                else:
                    pass
            elif appItem.appType == "RACK":
                tmpDCList = random.sample(appItem.dcList, 1)
                tmpID = tmpDCList[0]
                
                tmpRackList \
                        = self.faultTree.node[tmpID]['DATACENTER'].rackID
                
                self.faultTree = nx.union(self.faultTree\
                    .node[tmpID]['DATACENTER'].topology, appItem.topology)
                
                for i in range(len(appItem.pieceID)):
                    choiceList \
                            = random.sample(tmpRackList, appItem.replicaNum)
                    for j in range(appItem.replicaNum):
                        self.faultTree.add_edge(appItem.pieceID[i],\
                            choiceList[j])

                # computing the failure probability of datacenter
                if algorithm == "MC":
                    counter = 0.0
                    for i in range(0, TRIALS):
                        isHappen \
                            = self.get_failure_of_datacenter_via_mc(\
                            self.faultTree)
                        if isHappen == 1:
                            counter += 1.0
                    print(counter/float(TRIALS))
                elif algorithm == "Minimal":
                    self.get_failure_of_datacenter_via_mcs(self.faultTree)
                else:
                    pass
            else:
                pass

    def get_failure_of_datacenter_via_mc(self, dcTopo):
        #dcTopo = self.faultTree.node[node]['DATACENTER'].topology
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
            if dcTopo.node[item].keys()[0] == 'PIECE':
                dcTopo.node[item]['PIECE'].stickyBit = 0
                dcTopo.node[item]['PIECE'].happen = 0
            if dcTopo.node[item].keys()[0] == 'JOB':
                dcTopo.node[item]['JOB'].stickyBit = 0
                dcTopo.node[item]['JOB'].happen = 0
                
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
                if subSet:
                    dcTopo.node[item]['RACK'].happen = 1
                    dcTopo.node[item]['RACK'].cutSet.extend(subSet)
                    self.finalMinimalCut.extend(subSet)
                if dcTopo.node[item]['RACK'].happen == 0: 
                    self.finalMinimalCut = []
                    result = 0
                dcTopo.node[item]['RACK'].stickyBit = 1

        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'PIECE':
                neighborList = self.faultTree.neighbors(node)
                if self.faultTree.node[node]['PIECE'].stickyBit == 1:
                    continue
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= rackBase \
                            and neighborList[i] < accessBase:
                        if self.faultTree\
                           .node[neighborList[i]]['RACK'].happen == 0:
                            self.faultTree.node[node]['PIECE'].stickyBit = 1
                            self.faultTree.node[node]['PIECE'].happen = 0
                            break
                if i == len(neighborList):
                    self.faultTree.node[node]['PIECE'].happen = 1
                    self.faultTree.node[node]['PIECE'].stickyBit = 1
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'JOB':
                neighborList = self.faultTree.neighbors(node)
                if self.faultTree.node[node]['JOB'].stickyBit == 1:
                    continue
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= pieceBase \
                            and neighborList[i] < jobBase:
                        if self.faultTree\
                           .node[neighborList[i]]['PIECE'].happen == 1:
                            self.faultTree.node[node]['JOB'].stickyBit = 1
                            self.faultTree.node[node]['JOB'].happen = 1
                            result = 1
                            break
                if i == len(neighborList):
                    self.faultTree.node[node]['JOB'].happen = 0
                    result = 0
                    self.faultTree.node[node]['JOB'].stickyBit = 1
        return result

    # compute the failure probability via monte carol
    def get_failure_of_app_via_mc(self):
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
            if self.faultTree.node[node].keys()[0] == 'PIECE':
                self.faultTree.node[node]['PIECE'].stickyBit = 0
                self.faultTree.node[node]['PIECE'].happen = 0
            if self.faultTree.node[node].keys()[0] == 'JOB':
                self.faultTree.node[node]['JOB'].stickyBit = 0
                self.faultTree.node[node]['JOB'].happen = 0
                
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
                # The situation that data center's hardware fails
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER'].cutSet\
                        .append(self.faultTree.node[node]['DATACENTER'])
                if powerList:
                # The situation that data center's powers fail
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER']\
                            .cutSet.extend(powerList)
                if InternetList:
                # The situation that data center's Internet routers fail
                    self.faultTree.node[node]['DATACENTER'].happen = 1
                    self.faultTree.node[node]['DATACENTER']\
                            .cutSet.extend(InternetList)
                 
                if self.faultTree.node[node]['DATACENTER'].happen == 0:
                    result = 0                    
                self.faultTree.node[node]['DATACENTER'].stickyBit = 1
                
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'PIECE':
                neighborList = self.faultTree.neighbors(node)
                if self.faultTree.node[node]['PIECE'].stickyBit == 1:
                    continue
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= dcBase \
                            and neighborList[i] < routerBase:
                        if self.faultTree\
                           .node[neighborList[i]]['DATACENTER'].happen == 0:
                            self.faultTree.node[node]['PIECE'].stickyBit = 1
                            self.faultTree.node[node]['PIECE'].happen = 0
                            break
                if i == len(neighborList):
                    self.faultTree.node[node]['PIECE'].happen = 1
                    self.faultTree.node[node]['PIECE'].stickyBit = 1
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'JOB':
                neighborList = self.faultTree.neighbors(node)
                if self.faultTree.node[node]['JOB'].stickyBit == 1:
                    continue
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= pieceBase \
                            and neighborList[i] < jobBase:
                        if self.faultTree\
                           .node[neighborList[i]]['PIECE'].happen == 1:
                            self.faultTree.node[node]['JOB'].stickyBit = 1
                            self.faultTree.node[node]['JOB'].happen = 1
                            result = 1
                            break
                if i == len(neighborList):
                    self.faultTree.node[node]['JOB'].happen = 0
                    result = 0
                    self.faultTree.node[node]['JOB'].stickyBit = 1
        
        return result   


    def get_failure_of_datacenter_via_mcs(self, dcTopo):
        self.minimal_cut = []
        self.finalMinimalCut = []
        numbercounter = 0
        #dcTopo = self.faultTree.node[node]['DATACENTER'].topology
  
        # now we need to compute failure probability of datacenter
        result = 1.0
        routerPro = 1.0
        aggPro = 1.0
        switchPro = 1.0
        serverPro = 1.0
 
        # initialize a neighbor list
        neighborList = []
        subSet = []

        for item in dcTopo.node: 
            subSet = []
            if dcTopo.node[item].keys()[0] == 'AGGSWITCH':
                neighborList = dcTopo.neighbors(item)
                for i in range(0, len(neighborList)):
                    if neighborList[i] < item:
                        tmpR = dcTopo.node[neighborList[i]]['ROUTER']
                        subSet.append(tmpR)
                        if tmpR not in self.minimal_cut:
                            self.minimal_cut.append(tmpR)
                dcTopo.node[item]['AGGSWITCH'].cutSet.append(subSet)
                subSet = []
                subSet.append(dcTopo.node[item]['AGGSWITCH'])
                dcTopo.node[item]['AGGSWITCH'].cutSet.append(subSet)
        
        for item in dcTopo.node:
            subSet = []
            tmp = []
            if dcTopo.node[item].keys()[0] == 'RACK':
                neighborList = dcTopo.neighbors(item)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= aggBase \
                            and neighborList[i] < rackBase:
                        tmpA = dcTopo.node[neighborList[i]]['AGGSWITCH']
                        if not subSet:
                            subSet = list(tmpA.cutSet)
                        else:
                            tmpSubSet = list(subSet)
                            for j in range(0, len(subSet)):
                                for k in range(0, len(tmpA.cutSet)):
                                    tmp = list(subSet[j])
                                    #tmp.extend(tmpA.cutSet[k])
                                    if set(self.minimal_cut)\
                                            .issubset(set(tmp)) or\
                                       set(self.minimal_cut)\
                                            .issubset(set(tmpA.cutSet[k])):
                                        continue
                                    else:
                                        tmp.extend(tmpA.cutSet[k])
                                        tmpSubSet.append(tmp)
                                tmpSubSet.remove(subSet[j])
                            tmpSubSet.append(self.minimal_cut)
                            dcTopo.node[item]['RACK'].cutSet \
                                    = list(tmpSubSet)
                subSet = []
                subSet.append(dcTopo.node[item]['RACK'])
                dcTopo.node[item]['RACK'].cutSet.append(subSet)

        for item in dcTopo.node:       
            subSet = []
            if dcTopo.node[item].keys()[0] == 'PIECE':
                neighborList = dcTopo.neighbors(item)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= rackBase \
                            and neighborList[i] < pieceBase:
                        tmpR = dcTopo.node[neighborList[i]]['RACK']
                        if not subSet:
                            subSet = list(tmpR.cutSet)
                            dcTopo.node[item]['PIECE'].cutSet \
                                   = list(subSet)
                        else:
                            tmpSet = list(dcTopo.node[item]['PIECE'].cutSet)
                            for j in range(0, len(\
                                    dcTopo.node[item]['PIECE'].cutSet)):
                                for k in range(0, len(tmpR.cutSet)):
                                    tmp = list(dcTopo.node[item]['PIECE']\
                                            .cutSet[j])
                                    tmp.extend(tmpR.cutSet[k])
                                    tmpSet.append(tmp)
                                tmpSet.remove(dcTopo.node[item]['PIECE']\
                                        .cutSet[j])
                            dcTopo.node[item]['PIECE'].cutSet = list(tmpSet)

        for item in dcTopo.node:
            if dcTopo.node[item].keys()[0] == 'JOB':
                neighborList = dcTopo.neighbors(item)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= pieceBase \
                            and neighborList[i] < jobBase:
                        tmpP = dcTopo.node[neighborList[i]]['PIECE'] 
                        for j in range(0, len(tmpP.cutSet)):
                            dcTopo.node[item]['JOB'].cutSet\
                                    .append(tmpP.cutSet[j])
                self.finalMinimalCut = list(dcTopo.node[item]['JOB'].cutSet)
                break

        # minimal cut sets need to refine
        # this step removes redundant items
        for i in range(0, len(self.finalMinimalCut)):
            self.finalMinimalCut[i] = list(set(self.finalMinimalCut[i]))
        
        # enable all the cut sets to be the minimal
        baseList = list(self.finalMinimalCut)
        for i in range(0, len(baseList)):
            tmpListL = baseList[i]
            for j in range(i + 1, len(baseList)):
                tmpListR = baseList[j]
                if set(tmpListL).issubset(set(tmpListR)):
                    if tmpListR in self.finalMinimalCut:
                        self.finalMinimalCut.remove(tmpListR)
                        continue
                if set(tmpListR).issubset(set(tmpListL)):
                    if tmpListL in self.finalMinimalCut:
                        self.finalMinimalCut.remove(tmpListL)
        
        print("----- Minimal Cut Sets -----")
        print(self.finalMinimalCut)
        resultList = []
        for i in range(0, len(self.finalMinimalCut)):
            resultList.append(1.0)
        for i in range(0, len(self.finalMinimalCut)):
            #print('The %d minimal cut set:'%(i+1))
            #print("[")
            for j in range(0, len(self.finalMinimalCut[i])):
                #print('%s : %d'%(self.finalMinimalCut[i][j].typeName,\
                #        self.finalMinimalCut[i][j].ID))
                #print(self.finalMinimalCut[i][j].hardwareFailure)
                resultList[i] *= self.finalMinimalCut[i][j].hardwareFailure
            #print("]")
            #print('%f'%(resultList[i]))
        
        #self.faultTree.node[node]['DATACENTER'].cutSet \
        #        = self.finalMinimalCut
        '''
        tmpResult1 = 0.0
        tmpResult2 = 0.0
        result = 0.0
        
        for i in range(0, len(resultList)):
            tmpResult1 += resultList[i]
            for j in range(i + 1, len(resultList)):
                tmpResult2 += resultList[i] * resultList[j]
            
        result = tmpResult1
        '''
        tmpResult = 1.0
        for i in range(0, len(resultList)):
            tmpResult *= (1 - resultList[i])
        result = 1 - tmpResult

        print('The failure is: %f'%(result))

        return result
    
    def get_failure_of_app_via_mcs(self):
        neighborList = []
        self.finalMinimalCut = []
        appResult = []
        subSet = []
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
                self.faultTree.node[node]['DATACENTER'].failure = 0.047723
                #        = self.get_failure_of_datacenter(node)
                
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
        for node in self.faultTree.node:
            subSet = []
            if self.faultTree.node[node].keys()[0] == 'PIECE':
                neighborList = self.faultTree.neighbors(node)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= dcBase \
                            and neighborList[i] < pieceBase:
                        tmpD \
                        = self.faultTree.node[neighborList[i]]['DATACENTER']
                        if not subSet:
                            subSet = list(tmpD.cutSet)
                            self.faultTree.node[node]['PIECE'].cutSet\
                                    = list(subSet)
                        else:
                            tmpSet = list(self.faultTree\
                                    .node[node]['PIECE'].cutSet)
                            for j in range(0, len(self.faultTree\
                                    .node[node]['PIECE'].cutSet)):
                                for k in range(0, len(tmpD.cutSet)):
                                    tmp = list(self.faultTree\
                                            .node[node]['PIECE'].cutSet[j])
                                    tmp.extend(tmpD.cutSet[k])
                                    tmpSet.append(tmp)
                                tmpSet.remove(self.faultTree\
                                        .node[node]['PIECE'].cutSet[j])
                            self.faultTree.node[node]['PIECE'].cutSet \
                                    = list(tmpSet)
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'JOB':
                neighborList = self.faultTree.neighbors(node)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= pieceBase \
                            and neighborList[i] < jobBase:
                        tmpP = self.faultTree.node[neighborList[i]]['PIECE']
                        for j in range(0, len(tmpP.cutSet)):
                            self.faultTree.node[node]['JOB']\
                                    .cutSet.append(tmpP.cutSet[j])
                appResult = list(self.faultTree.node[node]['JOB'].cutSet)
                break

        # minimal cut sets need to refine
        tmpList = []
        for i in range(0, len(appResult)):
            appResult[i] = list(set(appResult[i]))
        
        # enable all the cut sets to be the minimal
        baseList = list(appResult)
        for i in range(0, len(baseList)):
            tmpListL = baseList[i]
            #print(baseList[i])
            for j in range(i+1, len(baseList)):
                if j >= len(baseList):
                    break
                tmpListR = baseList[j]
                if set(tmpListL).issubset(set(tmpListR)):
                    if tmpListR in appResult:
                        appResult.remove(tmpListR)
                elif set(tmpListR).issubset(set(tmpListL)):
                    if tmpListL in appResult:
                        appResult.remove(tmpListL)
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
    
    def get_failure_of_app_via_naive(self):
        neighborList = []
        finalResult = 1.0

        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'DATACENTER':
                powerFailure = 1.0
                routerFailure = 1.0

                neighborList = self.faultTree.neighbors(node)
                powerList = []
                InternetList = [] 
                
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= powerBase \
                            and neighborList[i] < InternetBase:
                        powerFailure *= self.faultTree\
                            .node[neighborList[i]]['POWERSTATION'].failure
                    if neighborList[i] >= InternetBase \
                            and neighborList[i] < dcBase:
                        routerFailure *= self.faultTree\
                            .node[neighborList[i]]['INTERNET'].failure
                
                self.faultTree.node[node]['DATACENTER'].failure \
                        = DEFAULT_FAILURE_OF_DC \
                        + powerFailure + routerFailure
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'PIECE':
                tmpPieceF = 1.0
                neighborList = self.faultTree.neighbors(node)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= dcBase \
                            and neighborList[i] < pieceBase:
                        tmpPieceF *= self.faultTree\
                             .node[neighborList[i]]['DATACENTER'].failure
                self.faultTree.node[node]['PIECE'].failure = tmpPieceF
        for node in self.faultTree.node:
            if self.faultTree.node[node].keys()[0] == 'JOB':
                neighborList = self.faultTree.neighbors(node)
                for i in range(0, len(neighborList)):
                    if neighborList[i] >= dcPiece \
                            and neighborList[i] < jobBase:
                        self.faultTree.node[node]['JOB'].failure \
                            += self.faultTree.node[neighborList[i]]\
                                                  ['PIECE'].failure
                finalResult = self.faultTree.node[node]['JOB'].failure
                break
        
        print(finalResult)
