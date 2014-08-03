from ft import *
from configuration import *
from tools import *
import Queue
import networkx as nx

class CRA:
    def __init__(self, tree):
        self.faultTree = tree
        self.minimalCutSet = []
        self.cutSet = []

    def minimal_cut_set_approach(self, tree, rootID):
        tmpList = []
        tmpList.append(tree.node[rootID].ID)
        self.minimalCutSet.append(tmpList)
        tmpQueue = Queue.Queue()
        tmpQueue.put(tree.node[rootID])
        while not tmpQueue.empty():
            tmpNode = tmpQueue.get()
            if len(tmpNode.childList) == 0:
                continue
            if tmpNode.gate == "OR":
                copyMinimalCutSet = list(self.minimalCutSet)
                for i in range(len(copyMinimalCutSet)):
                    if tmpNode.ID in copyMinimalCutSet[i]:
                        # iterating its children
                        for child in range(len(tmpNode.childList)):
                            tmpList = list(copyMinimalCutSet[i])
                            tmpList = [tmpNode.childList[child].ID\
                                    if x == tmpNode.ID \
                                    else x for x in tmpList]
                            self.minimalCutSet.append(tmpList)
                            tmpQueue.put(tmpNode.childList[child])
                        self.minimalCutSet.remove(copyMinimalCutSet[i])
            elif tmpNode.gate == "AND":
                for i in range(len(self.minimalCutSet)):
                    if tmpNode.ID in self.minimalCutSet[i]:
                        childIDList = []
                        for child in range(len(tmpNode.childList)):
                            childIDList.append(tmpNode.childList[child].ID)
                            tmpQueue.put(tmpNode.childList[child])
                        self.minimalCutSet[i].remove(tmpNode.ID)
                        self.minimalCutSet[i].extend(childIDList)
            else:
                pass

        # simplify our minimal cut sets
        # 1) remove redundancies
        for i in range(len(self.minimalCutSet)):
            self.minimalCutSet[i] = list(set(self.minimalCutSet[i]))
        
        # 2) get real minimal cut sets
        baseList = list(self.minimalCutSet)
        for i in range(len(baseList)):
            tmpListL = baseList[i]
            for j in range(i + 1, len(baseList)):
                if j >= len(baseList):
                    break
                tmpListR = baseList[j]
                if set(tmpListL).issubset(set(tmpListR)):
                    if tmpListR in self.minimalCutSet:
                        self.minimalCutSet.remove(tmpListR)
                elif set(tmpListR).issubset(set(tmpListL)):
                    if tmpListL in self.minimalCutSet:
                        self.minimalCutSet.remove(tmpListL)
                else:
                    pass
        self.minimalCutSet = sorted(self.minimalCutSet, key = len)
        print(self.minimalCutSet)

    def failure_sampling_approach(self, tree, rootID):        
        tmpStack = []
        tmpRoot = tree.node[rootID]
        tmpStack.append(tree.node[rootID])
        while tmpStack:
            if tmpStack[len(tmpStack) - 1].traverse == 0:
                tree.node[tmpStack[len(tmpStack) - 1].ID].traverse = 1
                tmpTopEle = tmpStack[len(tmpStack) - 1]                
                if tree.node[tmpTopEle.ID].childList:
                    for child in range(len(tree.node[tmpTopEle.ID]\
                            .childList)):
                        tmpStack.append(tree.node[tree.node[tmpTopEle.ID]\
                                .childList[child].ID])

                else:
                    if tree.node[tmpTopEle.ID].alreadySigned == 0:
                        tree.node[tmpTopEle.ID].happen \
                                = random_generator(0.5)
                        print('%s:%d'%(tmpTopEle.ID,tree.node[tmpTopEle.ID].happen))
                        for i in range(len(tree.node[tmpTopEle.ID]\
                                .parentList)):
                            tree.node[tmpTopEle.ID].parentList[i]\
                                    .childHappenList.append(\
                                    tree.node[tmpTopEle.ID])
                                    
                        tree.node[tmpTopEle.ID].alreadySigned = 1
                    tmpStack.pop()
            elif tmpStack[len(tmpStack) - 1].traverse == 1:
                if tmpStack[len(tmpStack) - 1].alreadySigned == 1:
                    tmpStack.pop()
                else:
                    if tmpStack[len(tmpStack) - 1].gate == "OR":
                        tmp = 0
                        ele = tmpStack[len(tmpStack) - 1]
                        for i in range(len(tree.node[ele.ID].childHappenList)):
                            if tree.node[tree.node[ele.ID].childHappenList[i].ID].happen == 1:
                                tree.node[ele.ID].happen = 1
                                tmp = 1
                                break
                        if tmp == 0:
                            tree.node[ele.ID].happen = 0

                        print('%s:%d'%(tree.node[ele.ID].ID,tree.node[ele.ID].happen))

                        for i in range(len(tree.node[ele.ID].parentList)):
                            tree.node[ele.ID].parentList[i]\
                                .childHappenList.append(tree.node[ele.ID])
                        tmpStack.pop()

                    elif tmpStack[len(tmpStack) - 1].gate == "AND":
                        tmp = 0
                        ele = tmpStack[len(tmpStack) - 1]
                        for i in range(len(tree.node[ele.ID].childHappenList)):
                            if tree.node[tree.node[ele.ID].childHappenList[i].ID].happen == 0:
                                tree.node[ele.ID].happen = 0
                                tmp = 1
                                break
                        if tmp == 0:
                            tree.node[ele.ID].happen = 1
                        for i in range(len(tree.node[ele.ID].parentList)):
                            tree.node[ele.ID].parentList[i]\
                                .childHappenList.append(tree.node[ele.ID])
                        tmpStack.pop()
                    else:
                        pass
        
        # let's get cut sets
        for item in tree:
            if not tree.node[item].childList \
                    and tree.node[item].happen == 1:
                self.cutSet.append(item)
        print(tree.node[rootID].happen)
        print(self.cutSet)

