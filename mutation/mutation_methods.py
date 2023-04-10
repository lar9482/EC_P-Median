"""
    Contains the implementations of 

    - Simple
    - Hyper Heuristic(A modification known as Nearest Four Neighbors)

    mutation methods that will be used in this project
"""

import numpy as np
import random
import math
import sys

def simple(chromosome, points):

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

def hyper_heuristic(chromosome, points):

    mutated_chromosome = chromosome.copy()

    non_selected_cities = np.where(chromosome == 0)[0]
    selected_cities = np.where(chromosome == 1)[0]

    #Scanning through all selected cities
    for city in selected_cities:

        #Getting its four nearest neighbors
        neighbors = get_four_neighbors(city, non_selected_cities, points)

        #Keeping a local minimum(chromosome and its associated fitness)
        best_chromosome = mutated_chromosome
        best_fitness = fitness_function(best_chromosome, points)

        #Scanning through the neighbors
        for neighbor_city in neighbors:

            #Constructing a chromosome with the neighbor included and the current city excluded
            possible_chromosome = mutated_chromosome.copy()
            possible_chromosome[city] = 0
            possible_chromosome[neighbor_city] = 1
            
            possible_fitness = fitness_function(possible_chromosome, points)

            #If the constructed chromosome has a better fitness, then keep track of it
            if (possible_fitness < best_fitness):
                best_fitness = possible_fitness
                best_chromosome = possible_chromosome
        
        #If the tracked local chromosome has a better fitness than the global chromosome,
        #keep track of the local chromosome from now on.
        if (best_fitness < fitness_function(mutated_chromosome, points)):
            mutated_chromosome = best_chromosome
    
    return mutated_chromosome


def get_four_neighbors(city, non_selected_cities, points):
    possible_cities = {}

    #Given the current city, calculate euclidean distance between all non-selected cities
    for possible_city in non_selected_cities:
        possible_cities[possible_city] = euclidean_distance(city, possible_city, points)
    sorted_possible_cities = dict(sorted(possible_cities.items(), key=lambda item: item[1]))

    #Get the four nearest cities of inputted 'city'
    return list(sorted_possible_cities.keys())[0:4:1]


##The fitness function is utilized in the hyper_heuristic mutation
def fitness_function(chromosome, points):

        #Get the city indices that have been selected(where they are 1)
        selected_cities = np.where(chromosome == 1)[0]

        #Keep track of the total minimum distances
        total_distance = 0

        #For every city in a particular chromosome
        for city in range(0, len(chromosome)):

            #Skip over cities that have been selected
            if (city in selected_cities):
                continue

            #Keep track of the minimum distance
            min_distance = sys.maxsize

            #Scanning through the selected cities, and get the minimum distance
            #between a current city and the all of the selected cities in the chromosome
            for selected_city in selected_cities:
                curr_distance = euclidean_distance(city, selected_city, points)
                if (curr_distance < min_distance):
                    min_distance = curr_distance

            total_distance += min_distance

        return total_distance

def euclidean_distance(curr_city, selected_city, points):
    x_term = (points[curr_city][0] - points[selected_city][0]) ** 2
    y_term = (points[curr_city][1] - points[selected_city][1]) ** 2
    return math.sqrt(x_term + y_term)