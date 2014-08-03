'''
Created on Sep 18, 2012

'''
import pickle

class Serilization:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def cloudToStream(self, cloudList):
        return pickle.dumps(cloudList)
    
    def streamToCloud(self, cloudStream):
        return pickle.loads(cloudStream)
