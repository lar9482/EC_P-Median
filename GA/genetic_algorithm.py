import numpy as np
import random
import sys
import math

class genetic_algorithm:
    """
        This constructor method will 
    """
    def __init__(self, p, n, points,
                       selection = None,
                       crossover = None,
                       mutation = None,
                       crossover_rate = None,
                       mutation_rate = None,
                       size = 100):
        self.p = p
        self.n = n
        self.points = points

        self.selection = selection

        self.crossover = crossover
        self.crossover_rate = crossover_rate
        
        self.mutation = mutation
        self.mutation_rate = mutation_rate

        self.population = self.__init_population(size)
        self.population_size = size

    """
        This function will initialize the population pool.
        @param size(int): The size to specify the population pool

        @returns (np.shape(size, n)): 
                 The initial population pool, 
                 with 'size' number of chromosomes that are of length 'n'
    """
    def __init_population(self, size):

        #Get a np array of (size, n) for the pool
        initial_population = np.empty((size, self.n), dtype=np.int32)

        #For every location for a chromosome
        for chromosome in range(0, size):

            #Get 'p' city locations that specify the 'median' cities of a chromosome
            selected_cities = {}
            #While there are less than 'p' cities selected
            while (len(selected_cities) < self.p):
                #Get a random city
                random_city = random.randint(0, self.n-1)
                #Ensure that a city hasn't been selected yet
                while ((random_city in selected_cities)):
                    random_city = random.randint(0, self.n-1)

                #Keep track of the selected city
                selected_cities[random_city] = random_city

            #Finally initialize a chromosome
            for city in range(0, self.n):

                #If the city has been selected, put 1 in the chromosome to indicate that
                #it's been 'selected'. Else, put 0 in the chromosome.
                if (city in selected_cities):
                    initial_population[chromosome, city] = 1
                else:
                    initial_population[chromosome, city] = 0

        return initial_population
    
    def calculate_raw_fitness(self):
        fitness_to_chromosome = {}

        #For every possible chromosome in the population pool, get its fitness
        #based on the specifications of the p-median problem
        for chromosome in range(0, self.population_size):
            
            #Get the city indices that have been selected(where they are 1)
            selected_cities = np.where(self.population[chromosome] == 1)[0]

            #Keep track of the total minimum distances
            total_distance = 0

            #For every city in a particular chromosome
            for city in range(0, len(self.population[chromosome])):

                #Skip over cities that have been selected
                if (city in selected_cities):
                    continue

                #Keep track of the minimum distance
                min_distance = sys.maxsize

                #Scanning through the selected cities, and get the minimum distance
                #between a 
                for selected_city in selected_cities:
                    curr_distance = self.__euclidean_distance(city, selected_city)
                    if (curr_distance < min_distance):
                        min_distance = curr_distance

                total_distance += min_distance
            
            #Store a fitness_chromosome pairing
            fitness_to_chromosome[total_distance] = self.population[chromosome]
        
        return dict(sorted(fitness_to_chromosome.items()))

    def __euclidean_distance(self, curr_city, selected_city):
        x_term = (self.points[curr_city][0] - self.points[selected_city][0]) ** 2
        y_term = (self.points[curr_city][1] - self.points[selected_city][1]) ** 2
        return math.sqrt(x_term + y_term)