'''
Job design

'''

from configuration import *
from cloud import *
import networkx as nx


class Job:
    '''
    Each job should have three properties: ID, components and failure
    '''
    def __init__(self, componentType, ID = 0):
        '''
        Constructor 
        self.load = 0.0   #double computation times per second (say 20/sec)
        self.timelimit = 0.0   #the upper bound time of a given job
        '''
	self.ID = ID
        self.dict_Component = {}
        self.dict_Component['SERVER'] \
             = {'CPU': 0.5, \
             'MEMORY': 100e6, \
               'DISK': 100e9, \
               'PORT': 1e6, \
              'POWER': True}
        #CPU:%, MEMORY: byte, DISK: Byte, PORT: byte/second, 
        self.dict_Component['RACK'] \
        = {'COMTASK': 1e12, 'TIMELIMIT': 100}   
        
        #ComputationTask: total numbers of computations, TimeLimit: second 
        self.dict_Component['AGGSWITCH'] \
        = {'COMTASK': 1e12, 'TIMELIMIT': 100}  
                
        self.dict_Component['ROUTER'] \
        =  {'COMTASK': 1e12, 'TIMELIMIT': 100}
	
        self.failure = DEFAULT_FAILURE_OF_JOB
	
class App:
    def __init__(self, jobNum, cloudList):
	self.topology = nx.Graph()
	dict_ID['JOB'] += 1
	self.jobID = dict_ID['JOB']

        self.topology.add_node(self.jobID)
	self.topology.node[self.jobID]['JOB'] = Job('SERVER', self.jobID)
        self.dcList = []

        for i in range(len(cloudList)):
            for dcItem in cloudList[i].topology.node:
                if cloudList[i].topology.node[dcItem].keys()[0]\
                   == 'DATACENTER':
                    self.dcList.append(dcItem)
                        
