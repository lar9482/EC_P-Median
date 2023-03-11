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
                       selection_adjustments = None,
                       crossover = None,
                       mutation = None,
                       crossover_rate = 1,
                       mutation_rate = 0.05,
                       size = 100):
        self.p = p
        self.n = n
        self.points = points

        self.selection = selection
        self.selection_adjustments = selection_adjustments

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
                #between a current city and the all of the selected cities in the chromosome
                for selected_city in selected_cities:
                    curr_distance = self.__euclidean_distance(city, selected_city)
                    if (curr_distance < min_distance):
                        min_distance = curr_distance

                total_distance += min_distance
            
            #Store a fitness_chromosome pairing
            if (not (total_distance in fitness_to_chromosome)):
                fitness_to_chromosome[total_distance] = [self.population[chromosome]]
            else:
                fitness_to_chromosome[total_distance].append(self.population[chromosome])
        
        return dict(sorted(fitness_to_chromosome.items(), reverse=True))

    def __euclidean_distance(self, curr_city, selected_city):
        x_term = (self.points[curr_city][0] - self.points[selected_city][0]) ** 2
        y_term = (self.points[curr_city][1] - self.points[selected_city][1]) ** 2
        return math.sqrt(x_term + y_term)
    
    def __get_elite_chromosomes(self, adjusted_fitness):

        #Getting the two best fittest values from the adjusted fitness pool
        #(Should be the last two entries since the pool is sorted)
        best_fitness = list(adjusted_fitness.keys())[len(adjusted_fitness)-1]
        next_best_fitness = list(adjusted_fitness.keys())[len(adjusted_fitness)-2]

        #Return the best chromosomes from the adjusted fitness pool
        return (
            adjusted_fitness[best_fitness],
            adjusted_fitness[next_best_fitness]
        )

    def run_algorithm(self, iterations = 1):

        for iteration in range(0, iterations):

            adjusted_fitness = self.selection_adjustments(
                self.calculate_raw_fitness(),
                self.population_size
            )
            new_population = np.array((self.population_size, self.n), dtype=np.int32)

            for pop_index in range(0, int(self.population_size/2)):

                child1 = np.empty((self.n), dtype=np.int32)
                child2 = np.empty((self.n), dtype=np.int32)

                if (pop_index == 0):
                    (child1, child2) = self.__get_elite_chromosomes(adjusted_fitness)
                else:
                    (parent1, parent2) = self.selection(adjusted_fitness)

                    if (random.uniform(0, 1) < self.crossover_rate):
                        (child1, child2) = self.crossover(parent1, parent2)
                    else:
                        (child1, child2) = (parent1, parent2)
                    print()
                print()