import numpy as np
import random

class genetic_algorithm:
    """
        This constructor method will 
    """
    def __init__(self, p, n, points,
                       crossover = None,
                       mutation = None,
                       crossover_rate = None,
                       mutation_rate = None,
                       size = 100):
        self.p = p
        self.n = n
        self.points = points

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
        for individual in range(0, size):

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
                    initial_population[individual, city] = 1
                else:
                    initial_population[individual, city] = 0

        return initial_population