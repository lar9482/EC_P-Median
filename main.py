from utils.file_io import load_dataset, graph_raw_points
from GA.genetic_algorithm import genetic_algorithm
from SA.simulated_annealing import simulated_annealing
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments
from crossover.crossover_methods import single_point, double_point, uniform
from mutation.mutation_methods import simple, hyper_heuristic

import matplotlib.pyplot as plt
import numpy as np

from utils.generate_dataset import generate_dataset
from utils.graph import graphing
from utils.file_io import save_stats

def test_selection():

    GA = genetic_algorithm(4, 20, load_dataset(4, 20), 
                           roulette, 
                           roulette_adjustments,
                           single_point)
    
    adjusted_fitness = roulette_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    roulette(adjusted_fitness)

    adjusted_fitness = rank_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    rank(adjusted_fitness)

    adjusted_fitness = touranment_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    touranment(adjusted_fitness)
    print()

def test_GA():
    p = 4
    n = 20
    points = load_dataset(p, n)

    GA = genetic_algorithm(p, 
                           n, 
                           points, 
                           roulette, 
                           roulette_adjustments,
                           single_point,
                           hyper_heuristic,
                           1,
                           0.05,
                           25)

    best_chromosome = GA.run_algorithm(20)
    best_fitness = GA.fitness_function(best_chromosome)
    stat_file_name = 'GA_P_{0}_N_{1}_results'.format(p, n)

    save_stats(roulette.__name__, 
               single_point.__name__, 
               hyper_heuristic.__name__, 
               best_fitness, 
               stat_file_name)
    graphing(best_chromosome, points, '7')


def test_SA():
    p = 8
    n = 72
    points = load_dataset(p, n)
    SA = simulated_annealing(p, n, points, simple, False)
    best_solution = SA.run_algorithm()
    graphing(best_solution, points)

def main():

    test_GA()

    # generate_dataset(p = 24)


if __name__ == "__main__":
    main()