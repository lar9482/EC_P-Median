from utils.file_io import load_dataset, graph_raw_points
from GA.genetic_algorithm import genetic_algorithm
from SA.simulated_annealing import simulated_annealing
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments
from crossover.crossover_methods import single_point, double_point, uniform
from mutation.mutation_methods import simple, hyper_heuristic

from utils.generate_dataset import generate_dataset
from utils.graph import graphing
from utils.file_io import save_GA_stats

from multiprocessing import Manager, Lock, Process

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

def old_test_GA():
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
    file_name = 'GA_P_{0}_N_{1}_results'.format(p, n)

    save_GA_stats(roulette.__name__, 
               single_point.__name__, 
               hyper_heuristic.__name__, 
               best_fitness, 
               file_name)
    graphing(best_chromosome, points, '7')

def run_GA(GA, iterations, points, lock):
    best_chromosome = GA.run_algorithm(iterations)

    best_fitness = GA.fitness_function(best_chromosome)
    stat_file_name = 'GA_P_{0}_N_{1}_results'.format(GA.p, GA.n)
    graph_file_name = 'P_{0}_N_{1}_{2}_{3}_{4}'.format(GA.p, GA.n, GA.selection.__name__, GA.crossover.__name__, GA.mutation.__name__)

    lock.acquire()
    save_GA_stats(GA.selection.__name__, 
                  GA.crossover.__name__, 
                  GA.mutation.__name__ ,
                  best_fitness, 
                  stat_file_name)
    lock.release()

    graphing(best_chromosome, points, graph_file_name)

def test_GA():
    #Constants
    pop_size = 50
    iterations = 100
    crossover_rate = 1
    mutation_rate = 0.05

    #Paramter options
    p_n_options = [(8, 72), (24, 600), (25, 650)]
    selections = [(roulette, roulette_adjustments), (rank, rank_adjustments), (touranment, touranment_adjustments)]
    crossovers = [single_point, double_point, uniform]
    mutations = [simple, hyper_heuristic]

    for p_n in p_n_options:
        for selection in selections:
            with Manager() as manager:
                all_processes = []
                lock = manager.Lock()
                points = load_dataset(p_n[0], p_n[1])
            
                for crossover in crossovers:
                    for mutation in mutations:
                        GA = genetic_algorithm( p_n[0], 
                                                p_n[1], 
                                                points, 
                                                selection[0], 
                                                selection[1],
                                                crossover,
                                                mutation,
                                                crossover_rate,
                                                mutation_rate,
                                                pop_size)
                        process = Process(target=run_GA, args=(
                                            GA, iterations, points, lock
                                         ))
                        all_processes.append(process)
                    
            #Start all of the subprocesses
            for process in all_processes:
                process.start()

            #Wait for all subprocesses to finish before continuing
            for process in all_processes:
                process.join()

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