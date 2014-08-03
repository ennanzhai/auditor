'''
This file aims to generate the concrete topology via the given cloud
configuration information

'''

import xml.dom.minidom
import networkx as nx
from cloud import *

class ModelGenerator:
    def __init__(self, xmlFile):

        # graph for topology
        self.topology = nx.Graph()
        
        # a few lists for various cloud components
        self.dcList = []
        self.powerList = []
        self.InternetList = []

        # read the given configuration file named xmlFile
        dom = xml.dom.minidom.parse(xmlFile)
        
        # obtain the root element, i.e., configuration tag
        root = dom.documentElement

        powerVec = root.getElementsByTagName('power')
        for item in powerVec:
            idTmpList = item.getElementsByTagName('ID')
            tmpID = int(idTmpList[0].childNodes[0].nodeValue)
            failureTmpList = item.getElementsByTagName('failure')
            tmpFailure = float(failureTmpList[0].childNodes[0].nodeValue)
            if not tmpID in self.powerList:
                self.powerList.append(tmpID)
                self.topology.add_node(tmpID)
                self.topology.node[tmpID]['POWERSTATION'] \
                        = PowerStation(tmpID, tmpFailure)
        
        InternetVec = root.getElementsByTagName('Internet')
        for item in InternetVec:
            idTmpList = item.getElementsByTagName('ID')
            tmpID = int(idTmpList[0].childNodes[0].nodeValue)
            failureTmpList = item.getElementsByTagName('failure')
            tmpFailure = float(failureTmpList[0].childNodes[0].nodeValue)
            if not tmpID in self.InternetList:
                self.InternetList.append(tmpID)
                self.topology.add_node(tmpID)
                self.topology.node[tmpID]['INTERNET'] \
                        = InternetProvider(tmpID, tmpFailure)

        dcVec = root.getElementsByTagName('datacenter')
        for dcItem in dcVec:
            idTmpList = dcItem.getElementsByTagName('ID')
            
            # datacenter ID
            tmpID = int(idTmpList[0].childNodes[0].nodeValue)
            failureTmpList = dcItem.getElementsByTagName('failure')
            tmpFailure = float(failureTmpList[0].childNodes[0].nodeValue)
            
            if tmpID in self.dcList:
                continue
            
            self.dcList.append(tmpID)
            self.topology.add_node(tmpID)
            self.topology.node[tmpID]['DATACENTER'] \
                    = DataCenter(tmpID, tmpFailure)
        
            depDCList = dcItem.getElementsByTagName('dep')
            for i in range(0, len(depDCList)):
                tmpDep = int(depDCList[i].childNodes[0].nodeValue)
                if tmpDep >= powerBase and tmpDep < dcBase:
                    self.topology.add_edge(tmpID, tmpDep)

            self.topology.node[tmpID]['DATACENTER'].topology = nx.Graph()

            # generating core routers
            coreVec = dcItem.getElementsByTagName('core')
            for item in coreVec:
                idCoreList = item.getElementsByTagName('ID')
                tmpCoreID = int(idCoreList[0].childNodes[0].nodeValue)
                failureCoreList = item.getElementsByTagName('failure')
                tmpCoreFailure \
                        = float(failureCoreList[0].childNodes[0].nodeValue)
        
                self.topology.node[tmpID]['DATACENTER'].routerID\
                        .append(tmpCoreID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .add_node(tmpCoreID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .node[tmpCoreID]['ROUTER'] \
                        = Router(tmpCoreID, tmpCoreFailure)
            
            aggVec = dcItem.getElementsByTagName('agg')
            for item in aggVec:
                idAggList = item.getElementsByTagName('ID')
                tmpAggID = int(idAggList[0].childNodes[0].nodeValue)
                failureAggList = item.getElementsByTagName('failure')
                tmpAggFailure \
                        = float(failureAggList[0].childNodes[0].nodeValue)
        
                self.topology.node[tmpID]['DATACENTER'].aggSwitchID\
                        .append(tmpAggID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .add_node(tmpAggID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .node[tmpAggID]['AGGSWITCH'] \
                        = AggSwitch(tmpAggID, tmpAggFailure)
                
                depAggList = item.getElementsByTagName('dep')
                for i in range(0, len(depAggList)):
                    tmpDep = int(depAggList[i].childNodes[0].nodeValue)
                    self.topology.node[tmpID]['DATACENTER'].topology\
                            .add_edge(tmpAggID, tmpDep)

            rackVec = dcItem.getElementsByTagName('rack')
            for item in rackVec:
                idRackList = item.getElementsByTagName('ID')
                tmpRackID = int(idRackList[0].childNodes[0].nodeValue)
                failureRackList = item.getElementsByTagName('failure')
                tmpRackFailure \
                        = float(failureRackList[0].childNodes[0].nodeValue)
        
                self.topology.node[tmpID]['DATACENTER'].rackID\
                        .append(tmpRackID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .add_node(tmpRackID)
                self.topology.node[tmpID]['DATACENTER'].topology\
                        .node[tmpRackID]['RACK'] \
                        = Rack(tmpRackID, tmpRackFailure)
                
                depRackList = item.getElementsByTagName('dep')
                for i in range(0, len(depRackList)):
                    tmpDep = int(depRackList[i].childNodes[0].nodeValue)
                    self.topology.node[tmpID]['DATACENTER'].topology\
                            .add_edge(tmpRackID, tmpDep)

