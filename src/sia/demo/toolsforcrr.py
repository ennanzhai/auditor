from random import random

def is_correlation():
    test = random.uniform(0,1)
    correlation_pro = 0.4
    if test < correlation_pro:
	return 1
    else:
	return 0

def change_failure_of_server(tree, from_server, to_server, failure):
    for node in tree.node:
	if tree.node[node].keys()[0] == 'SERVER':
	    if node <= to_server and node >= from_server:
		tree.node[node]['SERVER'].failure = failure

def change_failure_of_aggswitch(tree, from_agg, to_agg, failure):
    for node in tree.node:
	if tree.node[node].keys()[0] == 'AGGSWITCH':
	    if node <= to_server and node >= from_server:
		tree.node[node]['AGGSWITCH'].failure = failure

def change_failure_of_router(tree, from_router, to_router, failure):
    for node in tree.node:
	if tree.node[node].keys()[0] == 'ROUTER':
	    if node <= to_server and node >= from_server:
		tree.node[node]['ROUTER'].failure = failure

