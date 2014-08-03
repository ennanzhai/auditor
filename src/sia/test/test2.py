from ft_generator import *
import matplotlib.pyplot as plt
from cra import *
import sys

generator = FaultTreeGenerator(sys.argv[1])
#generator = FaultTreeGenerator("test2.xml")
c = CRA(generator.faultTree)
#c.minimal_cut_set_approach(generator.faultTree, "root123")
c.failure_sampling_approach(generator.faultTree, "root123")

'''
for i in generator.faultTree:
    print(generator.faultTree.node[i].ID)
    print(generator.faultTree.node[i].childList)
    print(generator.faultTree.node[i].parentList)
'''

'''
if __name__ == '__main__':

    generator = FaultTreeGenerator("tmp.xml")

    c = CRA(generator.faultTree)
    c.minimal_cut_set_approach(generator.faultTree, "root123")

    #nx.draw(generator.faultTree)
    #plt.show()
'''     
