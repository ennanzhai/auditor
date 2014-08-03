'''

The hardware component of the cloud generator

There are several hardwares here: 
1) cpu;
2) memory;
3) disk;
4) power;
5) port.

'''

# the definition of cpu class
class Cpu: 
    def __init__(self, init_corenum = 4, \
                 init_corefreq = 3.6e6, \
                 init_failure = 0.01):
        '''
        The CPU consists of core numbers, \
	core frequency and failure probability
        '''
        self.corenumber = init_corenum
        self.corefreq = init_corefreq
        self.failure = init_failure


# the definition of memory class        
class Memory:
    def __init__(self, init_size, \
                 init_rate, \
                 init_failure):
        '''
        The memory consists of size(Mb), rate(Mb/s) \
        and failure probability(0 to 1)
        '''               
        self.size = init_size
        self.rate = init_rate
        self.failure = init_failure


# the definition of disk class
class Disk:
    def __init__(self, init_size, \
                 init_failure):
        '''
        The Disk consists of size(MB) and failure probability
        '''
        self.size = init_size
        self.failure = init_failure


# the definition of power class
class Power:
    def __init__(self, init_failure):
        # The power consists of failure
        self.failure = init_failure


# the definition of port class
class Port:
    def __init__(self, init_rate, init_failure):
        '''
        Port consists of rate(Mb/s) and failure probability
        '''
        self.rate = init_rate
        self.failure = init_failure


# the definition of hardware class
class Hardware:
    def __init__(self, hardwareType):     
    	# hardwareType = {SERVER, SWITCH, AGGWITCH, ROUTER}  
        
        self.dict_Hardware = {}        
	# the initial values of server's hardware 
	self.dict_Hardware['RACK'] \
        = {'CPU': {'CORENUM': 4, 'COREFREQ': 3.6e6, 'FAILURE': 0.01},\
           'MEMORY': {'SIZE':256.0e6, 'RATE': 5.0e9, 'FAILURE': 0.02},\
           'DISK': {'SIZE': 1.0e12, 'FAILURE': 0.01},\
           'PORT': {'RATE': 3e6, 'FAILURE': 0.02},\
           'POWER': {'FAILURE': 0.001}\
        }
        
	# the initial values of switch's hardware
        self.dict_Hardware['SWITCH']\
	= {'CPU': {'CORENUM': 4, 'COREFREQ': 3.6e6, 'FAILURE': 0.01},\
	   'MEMORY': {'SIZE':256.0e6, 'RATE': 5.0e9, 'FAILURE': 0.02},\
           'DISK': {'SIZE': 1.0e12, 'FAILURE': 0.01},\
           'PORT': {'RATE': 3e6, 'FAILURE': 0.02},\
	   'POWER': {'FAILURE': 0.001}\
	}

	# the initial values of aggregation switch's hardware
        self.dict_Hardware['AGGSWITCH']\
	= {'CPU': {'CORENUM': 4, 'COREFREQ': 3.6e6, 'FAILURE': 0.01},\
	   'MEMORY': {'SIZE':256.0e6, 'RATE': 5.0e9, 'FAILURE': 0.02},\
	   'DISK': {'SIZE': 1.0e12, 'FAILURE': 0.01},\
	   'PORT': {'RATE': 3e6, 'FAILURE': 0.02},\
	   'POWER': {'FAILURE': 0.001}\
	}
        
	# the initial values of router's hardware
        self.dict_Hardware['ROUTER']\
	= {'CPU': {'CORENUM': 4, 'COREFREQ': 3.6e6, 'FAILURE': 0.01},\
	   'MEMORY': {'SIZE':256.0e6, 'RATE': 5.0e9, 'FAILURE': 0.02},\
	   'DISK': {'SIZE': 1.0e12, 'FAILURE': 0.01},\
	   'PORT': {'RATE': 3e6, 'FAILURE': 0.02},\
	   'POWER': {'FAILURE': 0.001}\
	}

	# passing the values to cpu object
        self.cpu = Cpu(self.dict_Hardware[hardwareType]['CPU']['CORENUM'],\
                       self.dict_Hardware[hardwareType]['CPU']['COREFREQ'],\
                       self.dict_Hardware[hardwareType]['CPU']['FAILURE'])

	# passing the values to memory object
        self.memory \
        = Memory(self.dict_Hardware[hardwareType]['MEMORY']['SIZE'],\
                 self.dict_Hardware[hardwareType]['MEMORY']['RATE'],\
                 self.dict_Hardware[hardwareType]['MEMORY']['FAILURE'])

	# passing the values to disk object
        self.disk = Disk(self.dict_Hardware[hardwareType]['DISK']['SIZE'],\
                    self.dict_Hardware[hardwareType]['DISK']['FAILURE'])

	# passing the values to port object
        self.port = Port(self.dict_Hardware[hardwareType]['PORT']['RATE'],\
                    self.dict_Hardware[hardwareType]['PORT']['FAILURE'])

	# passing the values to power object
        self.power \
        = Power(self.dict_Hardware[hardwareType]['POWER']['FAILURE'])

	self.failure = 1 - (1 - self.cpu.failure)\
			 * (1 - self.memory.failure)\
                         * (1 - self.disk.failure)\
                         * (1 - self.port.failure)\
                         * (1 - self.power.failure)         
