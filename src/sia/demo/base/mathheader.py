'''

This file only provide some functions for computation of math

'''
import random

def times_ele(element):
    re = 1.0
    i = 0
    for i in range(len(element)):
        re *= element[i]
    
    return re

def union_probability(element):
    return 1.0 - times_ele(element)

def random_generator(probability):
    pick = random.uniform(0, 1)
    if pick <= probability:
        return 1
    else:
        return 0

