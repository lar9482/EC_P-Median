import numpy as np
import random
import sys
import math

class genetic_algorithm:
    """
        This constructor method will initialize the genetic algorithm's global parameters

        @param p: Integer
            - The number of centers to look for in the dataset

        @param n: Integer
            - The number of points in the dataset

        @param points: list((Float, Float))
            - The dataset itself, consisting of a bunch of (x, y) points

        @param selection: F(dict(float: np.array{}))
            - The selection method for getting two chromosomes from the population pool

        @param selection_adjustments: F(dict(float: np.array), Integer)
            - The adjustment method used to transform raw fitness values into
              formats that are easily operatored on by the selection method

        @param crossover: F(np.array, np.array)
            - The crossover method for producing two children.
              This is used for exploiting what's known in the state space

        @param mutation: F(np.array)
            - The mutation method for editing 1 or one bits in a chromosome.
              This is used for exploring the state space

        @param crossover_rate: Float
            - The probability of performing a crossover.

        @param mutation_rate: Float
            - The probability of performing a mutation.

        @param size: Integer
            - The size of the population pool to work with.
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
        @param size: Integer 
            - The size to specify the population pool

        @returns (np.shape(size, n)): 
            - The initial population pool, 
              with 'size' number of chromosomes that are of length 'n'

              They represent a bitstring of exactly 'p' 1s.
    """
    def __init_population(self, size):

        #Get a np array of (size, n) for the pool
        initial_population = np.empty((size, self.n), dtype=np.int32)

        #For every location for a chromosome
        for chromosome_location in range(0, size):

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
                    initial_population[chromosome_location, city] = 1
                else:
                    initial_population[chromosome_location, city] = 0

        return initial_population
    
    """
        The actual fitness function for this genetic algorithm.
        For every vertex that is not selected(0s in the chromosome),
        the distance inbetween all selected vertices(1s in the chromosome) will be calculated, 
        which will the minimum distance to be returned.

        The fitness function will sum up the minimum distances inbetween all non-selected vertices and
        and the closest select vertices.

        @param chromosome(np.array((n))):
               The bitstring that represents selected(1) and non-selected(0) cities.
               NOTE: Each chromosome will be exactly 'p' 1s.

        @returns int:
                The sum of the minimum distances between all non-selected cities and the closest selected cities.
    """
    def fitness_function(self, chromosome):

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
                curr_distance = self.__euclidean_distance(city, selected_city)
                if (curr_distance < min_distance):
                    min_distance = curr_distance

            total_distance += min_distance

        return total_distance

    def __euclidean_distance(self, curr_city, selected_city):
        x_term = (self.points[curr_city][0] - self.points[selected_city][0]) ** 2
        y_term = (self.points[curr_city][1] - self.points[selected_city][1]) ** 2
        return math.sqrt(x_term + y_term)
    
    """
        This is a helper function that will calculate the fitness for all of the 
        chromosomes in the population pool.

        @returns (dict)
                 This dictionary contains fitness-chromosome pairings, 
                 where the key is the raw fitness
                 and the value is the chromosome associated with the raw fitness.
    """
    def calculate_raw_fitness(self):
        fitness_to_chromosome = {}

        #For every possible chromosome in the population pool, get its fitness
        #based on the specifications of the p-median problem
        for chromosome_index in range(0, self.population_size):

            #Getting the raw fitness of the current chromosome
            raw_fitness = self.fitness_function(self.population[chromosome_index])
            
            #Store a fitness_chromosome pairing
            if (not (raw_fitness in fitness_to_chromosome)):
                fitness_to_chromosome[raw_fitness] = [self.population[chromosome_index]]
            else:
                fitness_to_chromosome[raw_fitness].append(self.population[chromosome_index])
        
        #Return 'fitness_to_chromosome' pairings, which will be sorted from greatest fitness to least fitness
        return dict(sorted(fitness_to_chromosome.items(), reverse=True))

    
    
    def __get_elite_chromosomes(self, adjusted_fitness):

        #Getting the two best fittest values from the adjusted fitness pool
        #(Should be the last two entries since the pool is sorted)
        best_fitness = list(adjusted_fitness.keys())[len(adjusted_fitness)-1]
        next_best_fitness = list(adjusted_fitness.keys())[len(adjusted_fitness)-2]

        #Return the best chromosomes from the adjusted fitness pool
        return (
            adjusted_fitness[best_fitness][0],
            adjusted_fitness[next_best_fitness][0]
        )

    def __fixup_chromosome(self, child):
        replacement_child = child.copy()

        #While there are more selected cities than allowed
        #Remove cities that take away the maximium fitness from the chromosome
        while (np.sum(replacement_child) > self.p):

            #Getting indices that are 1 in the chromosome(selected cities)
            selected_cities = np.where(replacement_child == 1)[0]

            #Keep track of the max fitness and a possible child to return
            max_fitness = -sys.maxsize - 1 
            possible_child = np.empty((self.n), dtype=np.int32)

            for selected_city_index in selected_cities:

                #Create a copy of the passed in child, and set the 'selected' index to 0,
                #indicating that the current city is removed
                shorter_child = replacement_child.copy()
                shorter_child[selected_city_index] = 0
                shorter_fitness = self.fitness_function(shorter_child)
                
                if (shorter_fitness > max_fitness):
                    max_fitness = shorter_fitness
                    possible_child = shorter_child
            
            #Return the newly created child, which should have one city less
            replacement_child = possible_child

        #While there are less selected cities than allowed
        #Add cities that add the minimum possoble fitness to the chromosome
        while (np.sum(replacement_child) < self.p):

            #Getting indices that are 0 in the chromosome(non selected cities)
            non_selected_cities = np.where(replacement_child == 0)[0]

            #Keep track of the max fitness and a possible child to return
            min_fitness = sys.maxsize
            possible_child = np.empty((self.n), dtype=np.int32)

            for non_selected_city_index in non_selected_cities:

                #Create a copy of the passed in child, and set the 'selected' index to 1,
                #indicating that the current city is added
                longer_child = replacement_child.copy()
                longer_child[non_selected_city_index] = 1
                longer_fitness = self.fitness_function(longer_child)

                if (longer_fitness < min_fitness):
                    min_fitness = longer_fitness
                    possible_child = longer_child
            
            #Return the newly created child, which should more one city more
            replacement_child = possible_child

        return replacement_child
    
    def __best_chromosome(self, adjusted_fitness_chromosome_pool):
        chromosomes = list(adjusted_fitness_chromosome_pool.values())
        last_chromosome = chromosomes[len(chromosomes)-1][0]

        return last_chromosome
        
    def run_algorithm(self, epochs = 20):
        curr_best_chromosome = np.empty((self.n), dtype=np.int32)

        for epoch in range(0, epochs):

            #Getting the useful fitness using the fitness function
            #dict(adjusted_fitness(float): [chromosome]) #A dictionary from the fitness is key and chromosome is value
            adjusted_fitness = self.selection_adjustments(
                self.calculate_raw_fitness(),
                self.population_size
            )

            #Allocating a new population pool
            new_population_pool = np.empty((self.population_size, self.n), dtype=np.int32)

            for pop_index in range(0, int(self.population_size/2)):

                child1 = np.empty((self.n), dtype=np.int32)
                child2 = np.empty((self.n), dtype=np.int32)

                #At the beginning of a new generation, copy over the best 
                #chromosomes from the last generation.
                if (pop_index == 0):
                    (child1, child2) = self.__get_elite_chromosomes(adjusted_fitness)
                else:

                    #Select two chromosomes from the pool
                    (parent1, parent2) = self.selection(adjusted_fitness)

                    #Crossover the selected chromosomes
                    if (random.uniform(0, 1) < self.crossover_rate):
                        (child1, child2) = self.crossover(parent1, parent2)
                    else:
                        (child1, child2) = (parent1, parent2)
                    
                    #Fixup the chromosomes(i.e they do not have exactly 'p' 1 bits)
                    child1 = self.__fixup_chromosome(child1)
                    child2 = self.__fixup_chromosome(child2)

                    #Mutate the child chromosomes.
                    if (random.uniform(0, 1) < self.mutation_rate):
                        child1 = self.mutation(child1, self.points)
                    
                    if (random.uniform(0, 1) < self.mutation_rate):
                        child2 = self.mutation(child2, self.points)

                #Place the generated child into the new population pool
                new_population_pool[pop_index] = child1
                new_population_pool[pop_index + int(self.population_size/2)] = child2
            

            self.population = new_population_pool
            print('%s %s %s Generation: %s' % (self.selection.__name__, self.crossover.__name__, self.mutation.__name__, str(epoch+1)))
            curr_best_chromosome = self.__best_chromosome(adjusted_fitness)

            if (epoch % 10 == 0):
                print('Current best fitness')
                print(self.fitness_function(
                    curr_best_chromosome
                ))
                print()

        return curr_best_chromosome