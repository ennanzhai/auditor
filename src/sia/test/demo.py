import matplotlib.pyplot as plt
from cra import *
from dep_generator import *

if __name__ == '__main__':

    generator = DependencyGenerator("result.xml")
    
    #for node in generator.faultTree:
        #print generator.faultTree.node[node].ID
        #print generator.faultTree.node[node].gate
        #print generator.faultTree.node[node].parentList

    c = CRA(generator.faultTree)
    c.minimal_cut_set_approach(generator.faultTree, "service")

    nx.draw(generator.faultTree)
    plt.show()
