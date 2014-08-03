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

# dict_ID is used to denote the next available ID
global dict_ID
dict_ID = {
                'CLOUD': 0,
           'DATACENTER': 0, \
         'POWERSTATION': 0, \
             'INTERNET': 0, \
               'ROUTER': 0, \
            'AGGSWITCH': 0, \
                 'RACK': 0, \
               'SERVER': 0, \
               'SWITCH': 0, \
                'PIECE': 0, \
                  'JOB': 0,\
                  'APP': 0
          }

dict_ID['CLOUD'] = base * 0
dict_ID['POWERSTATION'] = base * 1
dict_ID['INTERNET'] = base * 2
dict_ID['DATACENTER'] = base * 3
dict_ID['ROUTER'] = base * 4
dict_ID['AGGSWITCH'] = base * 5
dict_ID['RACK'] = base * 6
dict_ID['SWITCH'] = base * 7
dict_ID['SERVER'] = base * 8
dict_ID['PIECE'] = base * 9
dict_ID['JOB'] = base * 10
dict_ID['APP'] = base * 11

global cloudBase 
cloudBase = base * 0

global powerBase
powerBase = base * 1

global InternetBase
InternetBase = base * 2

global dcBase
dcBase = base * 3

global routerBase
routerBase = base * 4

global aggBase
aggBase = base * 5

global rackBase
rackBase = base * 6

global accessBase
accessBase = base * 7

global serverBase
serverBase = base * 8

global pieceBase
pieceBase = base * 9

global jobBase
jobBase = base * 10

global appBase 
appBase = base * 11

'''
Some important default numbers for components

'''

# There should be 30 servers in a given rack
global DEFAULT_SERVER_NUM_IN_A_RACK
DEFAULT_SERVER_NUM_IN_A_RACK = 30

# There should be 1 access switch in a given rack
global DEFAULT_ACCSWITCH_NUM_IN_A_RACK
DEFAULT_ACCSWITCH_NUM_IN_A_RACK = 1

# There should be 10 core routers in a given datacenter
global DEFAULT_ROUTER_NUM_IN_A_DC
DEFAULT_ROUTER_NUM_IN_A_DC = 10

# There should be 20 aggregation switches in a given datacenter
global DEFAULT_AGGSWITCH_NUM_IN_A_DC
DEFAULT_AGGSWITCH_NUM_IN_A_DC = 20

# There should be 50 racks in a given datacenter
global DEFAULT_RACK_NUM_IN_A_DC
DEFAULT_RACK_NUM_IN_A_DC = 50

# There should be 10 power stations supporting a datacenter
global DEFAULT_POWER_NUM_FOR_A_DC
DEFAULT_POWER_NUM_FOR_A_DC = 10

# There should be 5 Internet providers supporting a datacenter
global DEFAULT_INTERNET_NUM_FOR_A_DC
DEFAULT_INTERNET_NUM_FOR_A_DC = 5

# There should be 30 power stations in a given cloud
global DEFAULT_POWER_NUM_IN_A_CLOUD
DEFAULT_POWER_NUM_IN_A_CLOUD = 30

# There should be 10 Internet providers in a given cloud
global DEFAULT_INTERNET_NUM_IN_A_CLOUD
DEFAULT_INTERNET_NUM_IN_A_CLOUD = 10

# There should be 10 datacenters in a cloud
global DEFAULT_DC_NUM_IN_A_CLOUD
DEFAULT_DC_NUM_IN_A_CLOUD = 10

'''

some important default failure probabilities

'''

# VM's default failure probability 
global DEFAULT_FAILURE_OF_VM
DEFAULT_FAILURE_OF_VM = 0.03

# Job's default failure probability
global DEFAULT_FAILURE_OF_JOB
DEFAULT_FAILURE_OF_JOB = 0.00

# Connections' failure probabilities
# Maybe we do not need this number any more
global DEFAULT_FAILURE_OF_CONNECTION
DEFAULT_FAILURE_OF_CONNECTION = 0.3

# 
global DEFAULT_FAILURE_OF_POWERSTATION
DEFAULT_FAILURE_OF_POWERSTATION = 0.15

global DEFAULT_FAILURE_OF_INTERNET
DEFAULT_FAILURE_OF_INTERNET = 0.111

global DEFAULT_FAILURE_OF_DC
DEFAULT_FAILURE_OF_DC = 0.047723

global TRIALS
TRIALS = 1000000
