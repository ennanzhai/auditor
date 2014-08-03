'''

This file is used to draw

'''

import matplotlib.pyplot as plt
import networkx as nx
from identity import *

def draw(ft, draw_type):
    if draw_type == "DATACENTER":
        G = nx.Graph()
        pos = { }
        labels={}
        G = ft

        i_for_power = 0.0
        i_for_router = 0.0
        i_for_dc = 0.0
        i_for_piece = 0.0
        i_for_app = 0.0

        nodeListDC = []
        nodeListRouter = []
        nodeListPiece = []
        nodeListPower = []
        nodeListApp = []

        for node in G:
            if G.node[node].keys()[0] == 'POWERSTATION':
                nodeListPower.append(node)
                pos[node] = (5 + i_for_power, 0.2)
                labels[node] = r'R'
                i_for_power += 30
            if G.node[node].keys()[0] == 'INTERNET':
                nodeListRouter.append(node)
                pos[node] = (10 + i_for_router, 0.4)
                labels[node] = r'Agg'
                i_for_router += 20
            if G.node[node].keys()[0] == 'DATACENTER':
                nodeListDC.append(node)
                pos[node] = (13 + i_for_dc, 0.6)
                labels[node] = r'RA'
                i_for_dc += 14
            '''
            if G.node[node].keys()[0] == 'PIECE':
                nodeListPiece.append(node)
                pos[node] = (13 + i_for_piece, 0.8)
                labels[node] = r'P'
                i_for_piece += 14
            if G.node[node].keys()[0] == 'JOB':
                nodeListApp.append(node)
                pos[node] = (20 + i_for_app, 1.0)
                labels[node] = r'JOB'
                i_for_app += 30
            '''
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListPower,\
               node_color = 'yellow', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListRouter,\
               node_color = 'orange', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListDC,\
           node_color = 'green', node_size = 400)
        #nx.draw_networkx_nodes(G, pos, nodelist = nodeListPiece,\
        #       node_color = 'green', node_size = 400)
        #nx.draw_networkx_nodes(G, pos, nodelist = nodeListApp,\
        #   node_color = 'yellow', node_size = 400)
        nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
        nx.draw_networkx_labels(G, pos, labels, font_size = 12)
    
    elif draw_type == "RACK":
        G = nx.Graph()
        pos = { }
        labels={}
        G = ft

        i_for_rack = 0.0
        i_for_router = 0.0
        i_for_agg = 0.0
        i_for_piece = 0.0
        i_for_app = 0.0

        nodeListRack = []
        nodeListRouter = []
        nodeListPiece = []
        nodeListAgg = []
        nodeListApp = []

        for node in G:
            if G.node[node].keys()[0] == 'ROUTER':
                nodeListRouter.append(node)
                pos[node] = (5 + i_for_router, 0.2)
                labels[node] = r'R'
                i_for_router += 30
            if G.node[node].keys()[0] == 'AGGSWITCH':
                nodeListAgg.append(node)
                pos[node] = (10 + i_for_agg, 0.4)
                labels[node] = r'Agg'
                i_for_agg += 20
            if G.node[node].keys()[0] == 'RACK':
                nodeListRack.append(node)
                pos[node] = (13 + i_for_rack, 0.6)
                labels[node] = r'RA'
                i_for_rack += 14
            if G.node[node].keys()[0] == 'PIECE':
                nodeListPiece.append(node)
                pos[node] = (13 + i_for_piece, 0.8)
                labels[node] = r'P'
                i_for_piece += 14
            if G.node[node].keys()[0] == 'JOB':
                nodeListApp.append(node)
                pos[node] = (20 + i_for_app, 1.0)
                labels[node] = r'JOB'
                i_for_app += 30

        nx.draw_networkx_nodes(G, pos, nodelist = nodeListRouter,\
               node_color = 'yellow', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListAgg,\
               node_color = 'orange', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListRack,\
           node_color = 'green', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListPiece,\
               node_color = 'green', node_size = 400)
        nx.draw_networkx_nodes(G, pos, nodelist = nodeListApp,\
           node_color = 'yellow', node_size = 400)
        nx.draw_networkx_edges(G, pos, width = 1.0, alpha = 1.0)
        nx.draw_networkx_labels(G, pos, labels, font_size = 12)
    else:
        pass

    plt.show()  

