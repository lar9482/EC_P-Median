import numpy as np
import random
import sys
import math

class simulated_annealing:

    """
        This constructor method will initialize the genetic algorithm's global parameters

        @param p: Integer
            - The number of centers to look for in the dataset

        @param n: Integer
            - The number of points in the dataset

        @param points: list((Float, Float))
            - The dataset itself, consisting of a bunch of (x, y) points

        @param pertubation: F(np.array)
            - The pertubation method for editing 1 or one bits in a solution.
              This is used for exploring the state space

        @param foolish: Boolean
            - This boolean tells the algorithm if it should be foolish or not
              That is, whether it should disregard all 'worse' solutions or not.
    """
    def __init__(self, p, n, points,
                       perturbation,
                       foolish = False):
        self.p = p
        self.n = n
        self.points = points

        self.perturbation = perturbation

        self.foolish = foolish

    def __fitness_function(self, solution):

        #Get the city indices that have been selected(where they are 1)
        selected_cities = np.where(solution == 1)[0]

        #Keep track of the total minimum distances
        total_distance = 0

        #For every city in a particular chromosome
        for city in range(0, len(solution)):

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
    
    def __generate_initial_solution(self):

        #Get a np array of (n, 1)
        initial_solution = np.empty((self.n), dtype=np.int32)

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
                initial_solution[city] = 1
            else:
                initial_solution[city] = 0

        return initial_solution

    def run_algorithm(self, alpha = 0.80, beta = 1.005):
        
        solution = self.__generate_initial_solution()
        T = 10
        max_epoch = 1000

        while (T >= 1):
            for epoch in range(0, int(max_epoch)):
                new_solution = self.perturbation(solution, self.points)

                old_fitness = self.__fitness_function(solution)
                new_fitness = self.__fitness_function(new_solution)
                if (new_fitness < old_fitness):
                    solution = new_solution
                elif (not self.foolish):
                    chance = random.uniform(0, 1)
                    chance_threshold = math.exp((old_fitness - new_fitness) / T)
                    if (chance < chance_threshold):
                        solution = new_solution
            T = alpha*T
            max_epoch = beta*max_epoch
            print(T)

        return solution
        