"""
    Contains the implementationsof 

    - Roulette
    - Rank
    - Touranment

    Selection to use in this project
"""

import copy
import random
def roulette(fitness_to_chromosome):

    #This dict will be worked with to store adjusted fitness values that
    #will be paired with the chromosomes inputted
    adjusted_fitness_chromosome = {}

    #Getting total raw fitness
    total_fitness = sum(list(fitness_to_chromosome.keys()))

    #Calculating (total_fitness / fitness) between all of the chromosomes
    for fitness in fitness_to_chromosome.keys():
        adjusted_fitness = (total_fitness) / (fitness)
        adjusted_fitness_chromosome[adjusted_fitness] = fitness_to_chromosome[fitness]

    #Getting a random fitness between the adjusted fitness
    min_fitness = min(list(adjusted_fitness_chromosome.keys()))
    max_fitness = max(list(adjusted_fitness_chromosome.keys()))
    roulette_fitness = random.uniform(min_fitness, max_fitness)

    #Scan through the adjusted fitness_chromosome pairings.
    #Once it detects a fitness that's less than the random fitness,
    #return that chromosome.
    for adjusted_fitness in adjusted_fitness_chromosome.keys():
        if (roulette_fitness < adjusted_fitness):
            return adjusted_fitness_chromosome[adjusted_fitness]
    


def rank(fitness_to_chromosome):

    fitness_chromosome = copy.deepcopy(fitness_to_chromosome)
    pass


def touranment(fitness_to_chromosome):

    fitness_chromosome = copy.deepcopy(fitness_to_chromosome)
    pass