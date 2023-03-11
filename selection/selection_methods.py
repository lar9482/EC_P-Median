"""
    Contains the implementationsof 

    - Roulette
    - Rank
    - Touranment

    Selection to use in this project
"""

import copy
import random
import numpy as np

def roulette_adjustments(fitness_to_chromosome, population_size):
    #This dict will be worked with to store adjusted fitness values that
    #will be paired with the chromosomes inputted
    adjusted_fitness_chromosome = {}

    #Getting total raw fitness
    total_fitness = sum(list(fitness_to_chromosome.keys()))

    #Calculating (total_fitness / fitness) between all of the chromosomes
    #, which is based for a minimizaation problem
    for fitness in fitness_to_chromosome.keys():
        adjusted_fitness_chromosome[(total_fitness) / (fitness)] = fitness_to_chromosome[fitness]

    return adjusted_fitness_chromosome

def roulette(adjusted_fitness_chromosome):

    #Getting a random fitness between the adjusted fitness
    min_fitness = min(list(adjusted_fitness_chromosome.keys()))
    max_fitness = max(list(adjusted_fitness_chromosome.keys()))

    chromosome1_roulette_fitness = random.uniform(min_fitness, max_fitness)
    chromosome2_roulette_fitness = random.uniform(min_fitness, max_fitness)

    chromosome1 = np.array((len(adjusted_fitness_chromosome)))
    chromosome2 = np.array((len(adjusted_fitness_chromosome)))

    #Scan through the adjusted fitness_chromosome pairings twice.
    #Once it detects a fitness that's less than the random fitness for the 1st/2nd chromosomes,
    #return that chromosome.
    for first_adjusted_fitness in adjusted_fitness_chromosome.keys():
        if (chromosome1_roulette_fitness < first_adjusted_fitness):
            chromosome1 = random.choice(adjusted_fitness_chromosome[first_adjusted_fitness])
            break
    
    for second_adjusted_fitness in adjusted_fitness_chromosome.keys():
        if (chromosome2_roulette_fitness < second_adjusted_fitness):
            chromosome2 = random.choice(adjusted_fitness_chromosome[second_adjusted_fitness])
            break

    return (chromosome1, chromosome2)
    
def rank_adjustments(fitness_to_chromosome, population_size):
    #This dict will be worked with to store adjusted ranking values that
    #will be paired with the chromosomes inputted
    rank_to_chromosome = {}

    #Getting the total rank from the population size
    total_rank = int(population_size * (population_size + 1) / 2)
    
    
    #Ranking all of the chromosomes inputted
    #based on a minimization problem
    curr_rank = 1
    for fitness in fitness_to_chromosome.keys():
        rank_to_chromosome[(curr_rank / total_rank)] = fitness_to_chromosome[fitness]
        curr_rank += 1

    return rank_to_chromosome

def rank(adjusted_fitness_chromosome):
    min_fitness = min(list(adjusted_fitness_chromosome.keys()))
    max_fitness = max(list(adjusted_fitness_chromosome.keys()))

    chromosome1_rank_fitness = random.uniform(min_fitness, max_fitness)
    chromosome2_rank_fitness = random.uniform(min_fitness, max_fitness)

    chromosome1 = np.array((len(adjusted_fitness_chromosome)))
    chromosome2 = np.array((len(adjusted_fitness_chromosome)))

    #Scan through the adjusted fitness_chromosome pairings twice.
    #Once it detects a fitness that's less than the random fitness for the 1st/2nd chromosomes,
    #return that chromosome.
    for first_adjusted_fitness in adjusted_fitness_chromosome.keys():
        if (chromosome1_rank_fitness < first_adjusted_fitness):
            chromosome1 = random.choice(adjusted_fitness_chromosome[first_adjusted_fitness])
            break
    
    for second_adjusted_fitness in adjusted_fitness_chromosome.keys():
        if (chromosome2_rank_fitness < second_adjusted_fitness):
            chromosome2 = random.choice(adjusted_fitness_chromosome[second_adjusted_fitness])
            break

    return (chromosome1, chromosome2)


def touranment(fitness_to_chromosome):

    fitness_chromosome = copy.deepcopy(fitness_to_chromosome)
    pass