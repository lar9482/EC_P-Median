"""
    Contains the implementations of 

    - Simple
    - Hyper Heuristic

    mutation methods that will be used in this project
"""


import numpy as np
import random

def simple(chromosome):

    #Basically, this method will swap values from two random indices
    #from the selected and non-selected cities in the chromosome
    
    mutated_chromosome = chromosome.copy()

    non_selected_cities = np.where(chromosome == 0)[0]
    selected_cities = np.where(chromosome == 1)[0]

    non_selected_city = random.choice(non_selected_cities)
    selected_city = random.choice(selected_cities)

    temp_selected_city = mutated_chromosome[selected_city]
    mutated_chromosome[selected_city] = mutated_chromosome[non_selected_city]
    mutated_chromosome[non_selected_city] = temp_selected_city
    
    return mutated_chromosome

def hyper_heuristic(chromosome):
    pass