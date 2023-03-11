from utils.file_io import load_dataset, graph_raw_points
from GA.genetic_algorithm import genetic_algorithm
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments

def main():
    p = 4
    n = 20
    points = load_dataset(p, n)

    GA = genetic_algorithm(p, n, points, roulette, roulette_adjustments)
    # test = GA.calculate_raw_fitness()

    # adjusted_fitness = roulette_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    # roulette(adjusted_fitness)

    # adjusted_fitness = rank_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    # rank(adjusted_fitness)

    adjusted_fitness = touranment_adjustments(GA.calculate_raw_fitness(), GA.population_size)
    touranment(adjusted_fitness)
    GA.run_algorithm()

    print()


if __name__ == "__main__":
    main()