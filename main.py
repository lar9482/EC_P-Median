from utils.file_io import load_dataset, graph_raw_points
from GA.genetic_algorithm import genetic_algorithm
from SA.simulated_annealing import simulated_annealing
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments
from crossover.crossover_methods import single_point, double_point, uniform
from mutation.mutation_methods import simple, hyper_heuristic

import matplotlib.pyplot as plt
import numpy as np

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

def quick_graphing(chromosome, points):
    selected = np.empty((len(np.where(chromosome == 1)[0]), 2))
    non_selected = np.empty((len(points) - len(np.where(chromosome == 1)[0]), 2)) 

    selected_i = 0
    non_selected_i = 0

    for i in range(0, len(chromosome)):
        if chromosome[i] == 1:
            selected[selected_i] = points[i]
            selected_i += 1
        else:
            non_selected[non_selected_i] = points[i]
            non_selected_i += 1
    
    plt.plot([x[0] for x in selected], [y[1] for y in selected], 'o', color='red')
    plt.plot([x[0] for x in non_selected], [y[1] for y in non_selected], 'o', color='blue')
    plt.xlim(-2,12)
    plt.ylim(-2,12)
    plt.xscale('linear')
    plt.yscale('linear')
    plt.show()

def test_GA():
    p = 8
    n = 72
    points = load_dataset(p, n)

    GA = genetic_algorithm(p, n, points, 
                           touranment, 
                           touranment_adjustments,
                           single_point,
                           hyper_heuristic,
                           1,
                           0.05,
                           50)

    best_chromosome = GA.run_algorithm(25)

    quick_graphing(best_chromosome, points)
def main():

    p = 8
    n = 72
    points = load_dataset(p, n)
    SA = simulated_annealing(p, n, points, simple, False)
    SA.run_algorithm()
    print()


if __name__ == "__main__":
    main()