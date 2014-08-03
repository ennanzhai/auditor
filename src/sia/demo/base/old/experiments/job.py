'''
Application design

'''

from configuration import *
from cloud import *
import networkx as nx

class Piece:
    '''
    Each job should have three properties: ID, components and failure
    '''
    def __init__(self, ID):
        # Assign a new ID to the piece
        self.ID = ID
        self.failure = 0.0
        self.stickyBit = 0
        self.happen = 0
        self.cutSet = []

class Job:
    def __init__(self, ID):
        self.ID = ID
        self.failure = 0.0
        self.stickyBit = 0
        self.happen = 0
        self.cutSet = []

class App:
    def __init__(self, pieceNum, replicaNum, appType, cloudList):
	# Assign a new ID to the application
        dict_ID['APP'] += 1
	self.ID = dict_ID['APP']

        # Generating a graph for the given application
	self.topology = nx.Graph()
        dict_ID['JOB'] += 1
        tmpID = dict_ID['JOB']
        self.topology.add_node(tmpID)
        self.topology.node[tmpID]['JOB'] = Job(tmpID)
	
        # Assign different values
        self.replicaNum = replicaNum
        self.appType = appType
        self.pieceNum = pieceNum
        self.dcList = []
        self.pieceID = []

        # Build topology for the given application
        # Connect the application node with each of the pieces
        jobID = tmpID
        for i in range(pieceNum):
            dict_ID['PIECE'] += 1
            tmpID = dict_ID['PIECE']
            self.pieceID.append(tmpID)
            self.topology.add_node(tmpID)
            self.topology.node[tmpID]['PIECE'] = Piece(tmpID)
            self.topology.add_edge(jobID, tmpID)
        
        for i in range(len(cloudList)):
            for dcItem in cloudList[i].topology.node:
                if cloudList[i].topology.node[dcItem].keys()[0]\
                        == 'DATACENTER':
                    self.dcList.append(dcItem)
