"""
    Contains the implementations of 

    - Single Point
    - Double Point
    - Uniform

    crossover methods that will be used in this project
"""

import random
import numpy as np

def single_point(parent1, parent2):
    splice_point = int(random.uniform(1, len(parent1)-1))

    child1 = np.concatenate((parent1[0:splice_point:1], parent2[splice_point:len(parent2):1]))
    child2 = np.concatenate((parent2[0:splice_point:1], parent1[splice_point:len(parent1):1]))

    return (child1, child2)

def double_point(parent1, parent2):
    pass

def uniform(parent1, parent2):
    pass