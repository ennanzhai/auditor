'''

This is the cloud generator. 
Cloud generator mainly aims to generate the cloud graph

'''
from cloud import *

class CloudGenerator: 
    def __init__(self):
        self.cloudList = []
	self.saasList = []
	self.appList = []
    
    # This API is mainly for generating cloud    
    def cloudGenerator(self, cloudNum, saasNum, jobNum):
	for i in range(cloudNum):
            # one datacenter, two routers, two agg switches and two racks
            # there are two servers in each rack
	    c = Cloud(1, 2, 2, 2, 2)
	    self.cloudList.append(c)
	for i in range(saasNum):
            # we have saasNum SaaS and there is one service in each of them
	    s = SaaS(1)
	    self.saasList.append(s)
	for i in range(jobNum):
            # we have jobNum jobs and there are six VMs in each of them
	    a = App(6)
            self.appList.append(a)
    
