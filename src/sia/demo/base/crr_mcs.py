
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
        self.minimal_cut = []
        self.finalMinimalCut = []
        numbercounter = 0
        dcTopo = self.faultTree.node[node]['DATACENTER'].topology
  
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
                    if neighborList[i] < item:
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
                                        print(numbercounter)
                                        numbercounter += 1                                        
                                        tmpSubSet.append(tmp)
                                tmpSubSet.remove(subSet[j])
                            tmpSubSet.append(self.minimal_cut)
                            dcTopo.node[item]['RACK'].cutSet \
                                    = list(tmpSubSet)
                subSet = []
                subSet.append(dcTopo.node[item]['RACK'])
                dcTopo.node[item]['RACK'].cutSet.append(subSet)
                
                #print("-----------")
                #print(dcTopo.node[item]['SWITCH'].cutSet)    

                if not self.finalMinimalCut:
                    self.finalMinimalCut = list(dcTopo.node[item]['RACK']\
                            .cutSet)
                else:
                    keepSet = list(self.finalMinimalCut)
                    for i in range(0, len(keepSet)):
                        for j in range(0, len(dcTopo.node[item]['RACK']\
                                .cutSet)):
                            tmp = list(keepSet[i])
                            if set(self.minimal_cut).issubset(set(tmp))\
                               or \
                               set(self.minimal_cut)\
                               .issubset(\
                               set(dcTopo.node[item]['RACK'].cutSet[j])):
                                continue
                            else:
                                tmp.extend(dcTopo.node[item]['RACK']\
                                        .cutSet[j])
                                print(numbercounter)
                                numbercounter += 1
                                self.finalMinimalCut.append(tmp)
                                if keepSet[i] in self.finalMinimalCut:
                                    self.finalMinimalCut.remove(keepSet[i])
        
        
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
                    if tmpListL in self.finalMinimalCut:
                        self.finalMinimalCut.remove(tmpListR)
                        continue
                if set(tmpListR).issubset(set(tmpListL)):
                    if tmpListR in self.finalMinimalCut:
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
        
        self.faultTree.node[node]['DATACENTER'].cutSet \
                = self.finalMinimalCut
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
                self.faultTree.node[node]['DATACENTER'].failure\
                        = self.get_failure_of_datacenter(node)
                
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
                    if tmpListL in appResult:
                        appResult.remove(tmpListR)
                elif set(tmpListR).issubset(set(tmpListL)):
                    if tmpListR in appResult:
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

