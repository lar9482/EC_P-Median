from utils.file_io import load_dataset, graph_raw_points
from GA.genetic_algorithm import genetic_algorithm
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments
from crossover.crossover_methods import single_point, double_point, uniform
from mutation.mutation_methods import simple, hyper_heuristic


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


def main():
    p = 8
    n = 72
    points = load_dataset(p, n)

    GA = genetic_algorithm(p, n, points, 
                           touranment, 
                           touranment_adjustments,
                           single_point,
                           simple,
                           1,
                           0.05,
                           50)

    best_one = GA.run_algorithm(30)

    print()


if __name__ == "__main__":
    main()