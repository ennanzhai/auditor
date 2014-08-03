from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import networkx as nx
from ft import *

class FaultTreeGenerator:
    def __init__(self, xmlFile):
        document = ElementTree.parse(xmlFile)
        root = document.getroot()

        pathList = []
        self.faultTree = nx.Graph()
        rootID = "root123"
        self.faultTree.add_node(rootID)
        self.faultTree.node[rootID] = TreeNode()
        self.faultTree.node[rootID].ID = rootID
        self.faultTree.node[rootID].gate = "AND"

        # put all the paths in pathList
        for child in root:
            path = []
            tmpS = child.attrib['rout']
            path = tmpS.split(',')
            tmpSrc = child.attrib['src']
            path.insert(0, tmpSrc)
            tmpDst = child.attrib['dst']
            path.append(tmpDst)
            pathList.append(path)

        pathID = "0"
        for itemList in range(len(pathList)):
            tmpNode = TreeNode()
            tmpPathID = int(pathID) + 1
            tmpNode.ID = str(tmpPathID)
            pathID = str(tmpPathID)
            tmpNode.gate = "OR"
        
            for i in range(len(pathList[itemList])):
                tmpChild = TreeNode()
                tmpChild.ID = pathList[itemList][i]
                tmpNode.childList.append(tmpChild)
                #tmpChild.parentList.append(tmpNode)

            self.faultTree.node[rootID].childList.append(tmpNode)
            tmpNode.parentList.append(self.faultTree.node[rootID])

            self.faultTree.add_edge(rootID, tmpNode.ID)
            self.faultTree.node[tmpNode.ID] = tmpNode

            for i in range(len(tmpNode.childList)):
                self.faultTree.add_edge(tmpNode.ID, tmpNode.childList[i].ID)
                self.faultTree.node[tmpNode.childList[i].ID] \
                        = tmpNode.childList[i]
        
        for item in self.faultTree:
            if not self.faultTree.node[item].childList:
                neighborList = self.faultTree.neighbors(item)
                for i in range(len(neighborList)):
                    self.faultTree.node[item].parentList\
                            .append(self.faultTree.node[neighborList[i]])
