"""
    Contains the implementations of 

    - Single Point
    - Double Point
    - Uniform

    crossover methods that will be used in this project
"""

import random
import numpy as np

def crossover_feasibility(parent1, parent2):
    if (len(parent1) != len(parent2)):
        raise Exception('ERROR: Two inputted parents cannot be crossed over')
    
def single_point(parent1, parent2):
    crossover_feasibility(parent1, parent2)

    splice_point = int(random.uniform(1, len(parent1)-1))

    child1 = np.concatenate((parent1[0:splice_point:1], parent2[splice_point:len(parent2):1]))
    child2 = np.concatenate((parent2[0:splice_point:1], parent1[splice_point:len(parent1):1]))

    return (child1, child2)

def double_point(parent1, parent2):
    crossover_feasibility(parent1, parent2)

    first_splice_point = int(random.uniform(0, len(parent1)-2))
    second_splice_point = int(random.uniform(first_splice_point, len(parent1)-1))

    child1 = np.concatenate((parent1[0:first_splice_point:1], parent2[first_splice_point:second_splice_point:1])) 
    child1 = np.concatenate((child1, parent1[second_splice_point:len(parent1):1]))

    child2 = np.concatenate((parent2[0:first_splice_point:1], parent1[first_splice_point:second_splice_point:1]))
    child2 = np.concatenate((child2, parent2[second_splice_point:len(parent2):1]))
    
    return(child1, child2)

def uniform(parent1, parent2):
    crossover_feasibility(parent1, parent2)
    
    uniform_bitstring = np.empty((len(parent1)), dtype=np.int32)

    for i in range(0, len(uniform_bitstring)):
        if (random.uniform(0, 1) < 0.5):
            uniform_bitstring[i] = 0
        else:
            uniform_bitstring[i] = 1

    pass