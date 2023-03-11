from utils.file_io import load_dataset, graph_raw_points

from GA.genetic_algorithm import genetic_algorithm
def main():
    p = 4
    n = 20
    points = load_dataset(p, n)

    GA = genetic_algorithm(p, n, points)
    test = GA.calculate_raw_fitness()
    print()


if __name__ == "__main__":
    main()