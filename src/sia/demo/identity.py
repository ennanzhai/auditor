'''
ID notation rule: 
    Cloud:          0
    DataCenter:     1 + 0000000000
    Router:         2 + 0000000000
    AggSwitch:      3 + 0000000000
    Rack:           4
    Switch:         5
    PowerStation:   6
    Server:         7
    Service:        8
    Saas:           9
    VM:             10
    Job:            11

'''

'''

base variables are used to compute ID

'''

global base
base = 10000000000

global cloud_base
cloud_base = 0

global datacenter_base
datacenter_base = cloud_base + 1

global router_base
router_base = datacenter_base + 1

global aggswitch_base
cloud_base = 0

# dict_ID is used to denote the next available ID
global dict_ID
dict_ID = {
                'CLOUD': 0,
           'DATACENTER': 0, \
               'ROUTER': 0, \
            'AGGSWITCH': 0, \
                 'RACK': 0, \
               'SERVER': 0, \
         'POWERSTATION': 0, \
               'SWITCH': 0, \
                   'VM': 0, \
                  'JOB': 0, \
		 'SAAS': 0, \
	      'SERVICE': 0 }

dict_ID['CLOUD'] = base * 0
dict_ID['DATACENTER'] = base * 1
dict_ID['ROUTER'] = base * 2
dict_ID['AGGSWITCH'] = base * 3
dict_ID['RACK'] = base * 4
dict_ID['SWITCH'] = base * 5
dict_ID['POWERSTATION'] = base * 6
dict_ID['SERVER'] = base * 7
dict_ID['SERVICE'] = base * 8
dict_ID['SAAS'] = base * 9
dict_ID['VM'] = base * 10
dict_ID['JOB'] = base * 11

'''

Some important default numbers for components

'''

global DEFAULT_SERVER_NUM_IN_A_RACK
DEFAULT_SERVER_NUM_IN_A_RACK = 30

global DEFAULT_ACCSWITCH_NUM_IN_A_RACK
DEFAULT_ACCSWITCH_NUM_IN_A_RACK = 1

global DEFAULT_ROUTER_NUM_IN_A_DC
DEFAULT_ROUTER_NUM_IN_A_DC = 10

global DEFAULT_AGGSWITCH_NUM_IN_A_DC
DEFAULT_AGGSWITCH_NUM_IN_A_DC = 20

global DEFAULT_RACK_NUM_IN_A_DC
DEFAULT_RACK_NUM_IN_A_DC = 50

global DEFAULT_POWER_NUM_IN_A_DC
DEFAULT_POWER_NUM_IN_A_DC = 20

'''

some important default failure probabilities

'''

global DEFAULT_FAILURE_OF_VM
DEFAULT_FAILURE_OF_VM = 0.03

global DEFAULT_FAILURE_OF_JOB
DEFAULT_FAILURE_OF_JOB = 0.00


