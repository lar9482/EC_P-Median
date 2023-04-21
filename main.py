from utils.file_io import load_dataset
from GA.genetic_algorithm import genetic_algorithm
from SA.simulated_annealing import simulated_annealing
from selection.selection_methods import roulette, roulette_adjustments, rank, rank_adjustments, touranment, touranment_adjustments
from crossover.crossover_methods import single_point, double_point, uniform
from mutation.mutation_methods import simple, hyper_heuristic

from utils.generate_dataset import generate_dataset
from utils.graph import graphing
from utils.file_io import save_GA_stats, save_SA_stats

from multiprocessing import Manager, Lock, Process

def run_GA(GA, iterations, points, lock):

    #Run the algorithm and get the best chromosome
    best_chromosome = GA.run_algorithm(iterations)

    #Get fitness associated with best chromosome
    best_fitness = GA.fitness_function(best_chromosome)

    #Given the parameters, format the file name for the statistics and graph files.
    stat_file_name = 'GA_P_{0}_N_{1}_results'.format(GA.p, GA.n)
    graph_file_name = 'P_{0}_N_{1}_{2}_{3}_{4}'.format(GA.p, GA.n, GA.selection.__name__, GA.crossover.__name__, GA.mutation.__name__)

    #Save the stats and graph the best chromosome.
    lock.acquire()
    save_GA_stats(GA.selection.__name__, 
                  GA.crossover.__name__, 
                  GA.mutation.__name__ ,
                  best_fitness, 
                  stat_file_name)
    graphing(best_chromosome, points, graph_file_name)
    lock.release()
    

def test_GA():
    #Constants
    pop_size = 25
    iterations = 100
    crossover_rate = 1
    mutation_rate = 0.05

    #Paramter options
    p_n_options = [(14, 210), (15, 240)]
    selections = [(roulette, roulette_adjustments), (rank, rank_adjustments)]
    crossovers = [single_point, double_point, uniform]
    mutations = [simple, hyper_heuristic]


    #Scanning through all possible p/n combinations and selection method options
    for p_n in p_n_options:
        for selection in selections:

            #For every crossover and mutation method combination, run the genetic algorithm on a subprocess
            with Manager() as manager:
                all_processes = []
                lock = manager.Lock()
                
                for crossover in crossovers:
                    for mutation in mutations:
                        points = load_dataset(p_n[0], p_n[1])
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

def old_test_SA():
    p = 4
    n = 20
    points = load_dataset(p, n)
    SA = simulated_annealing(p, n, points, simple, False)
    best_solution = SA.run_algorithm()
    graphing(best_solution, points)

def run_SA(SA, points, alpha, beta, lock):
    best_solution = SA.run_algorithm(alpha, beta)
    best_fitness = SA.fitness_function(best_solution)
    #Given the parameters, format the file name for the statistics and graph files.
    stat_file_name = 'SA_P_{0}_N_{1}_results'.format(SA.p, SA.n)
    graph_file_name = 'SA_P_{0}_N_{1}_{2}_{3}'.format(SA.p, SA.n, SA.perturbation.__name__, SA.foolish)

    lock.acquire()
    save_SA_stats(SA.foolish, 
                  SA.perturbation.__name__,
                  best_fitness, 
                  stat_file_name)
    graphing(best_solution, points, graph_file_name)
    lock.release()


def test_SA():

    #Constants for simulated annealing
    alpha = 0.95
    beta = 1.01

    #Parameter options for simulated annealing
    p_n_options = [(8, 72), (14, 210), (15, 240)]
    pertubations = [simple, hyper_heuristic]
    foolish_options = [True, False]

    for p_n in p_n_options:

        with Manager() as manager:
            all_processes = []
            lock = manager.Lock()

            for pertubation in pertubations:
                for foolish_option in foolish_options:
                    points = load_dataset(p_n[0], p_n[1])
                    SA = simulated_annealing(
                        p_n[0],
                        p_n[1],
                        points,
                        pertubation,
                        foolish_option
                    )
                    process = Process(target=run_SA, args=(
                                            SA, points, alpha, beta, lock
                                         ))
                    all_processes.append(process)
            
            #Start all of the subprocesses
            for process in all_processes:
                process.start()

            #Wait for all subprocesses to finish before continuing
            for process in all_processes:
                process.join()

def main():

    #test_GA()
    # test_SA()
    old_test_SA()
    # generate_dataset(p = 15)


if __name__ == "__main__":
    main()