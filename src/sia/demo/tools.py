import random

def is_correlation():
    test = random.uniform(0,1)
    correlation_pro = 0.4
    if test < correlation_pro:
	return 1
    else:
	return 0
