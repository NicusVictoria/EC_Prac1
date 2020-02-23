import random
from statistics import mean, stdev
from sys import argv
from time import process_time

import params
from Crossover import uniform_crossover, two_point_crossover, compete
from Plot import read_file
from individual import trap_function_non_linked, trap_function_linked, counting_ones
from params import generations, datapoints, population_size
from population import Population, create_initial_population
from printer import log_exp, log1, log2, log3


def create_next_generation(p, xover, ff, log=None):
    random.shuffle(p.population)
    new_population = Population()
    updated = False
    selection_errors = 0
    selection_correct = 0

    for i in range(0, len(p.population), 2):
        parent1 = p.population[i]
        parent2 = p.population[i + 1]
        parent1.generation = "parent"
        parent2.generation = "parent"
        child1, child2 = xover(parent1, parent2, ff)
        best, update, error, correct = compete(parent1, parent2, child1, child2)
        selection_correct += correct
        selection_errors += error
        updated = updated or update
        new_population.population += best

    new_population.set_fitness()
    if log == "2":
        return new_population, updated, selection_errors, selection_correct
    return new_population, updated


def run_generations(xover, ff, popsize, log):
    number_of_generations = []
    evaluations = []

    pop = Population()
    pop.population = create_initial_population(popsize, ff)
    pop.set_fitness()

    stopped = False
    generation_successful = True

    for i in range(generations):

        if log == "2":
            p, updated, errors, corrects = create_next_generation(pop, xover, ff, log)
            log2([xover.__name__, i, errors, corrects])
            if p.fitness == 100.00:
                print(p.fitness)
                return True

        else:
            p, updated = create_next_generation(pop, xover, ff)

        if log == "3":
            schema_zero = 0
            schema_one = 0
            fitnesses_s0 = []
            fitnesses_s1 = []

            for x in p.population:
                if x.genotype[0] == 0:
                    schema_zero += 1
                    f = ff(x.genotype)
                    fitnesses_s0.append(f)
                else:
                    schema_one += 1
                    fitnesses_s1.append(ff(x.genotype))

            if len(fitnesses_s0) < 2:
                mean_f_s0 = ""
                sdev_f_s0 = 0
            else:
                mean_f_s0 = mean(fitnesses_s0)
                sdev_f_s0 = stdev(fitnesses_s0)

            log3([xover.__name__, i,
                  schema_zero, schema_one,
                  mean_f_s0, sdev_f_s0,
                  mean(fitnesses_s1), stdev(fitnesses_s1)])

            if p.fitness == 100.00:
                print(p.fitness)
                return True

        if log == "1":
            ones = 0
            for pp in pop.population:
                ones += counting_ones(pp.genotype)
            log1([xover.__name__, i, (ones / population_size) / 100])

            if ones == population_size * 100:
                print(p.fitness)
                return True

        if p.best.fitness == 100 and (log != "1" and log != "2" and log != "3"):
            if log == "experiment":
                number_of_generations.append(i)
                evaluations.append(i * (popsize / 2))
                stopped = True
                break
            return True
        if not updated:
            # print("optimization unsuccessful")
            if log == "experiment":
                number_of_generations.append(i)
                evaluations.append(i * (popsize / 2))
                generation_successful = False
                stopped = True
                break
            return False
        pop = p

    if log == "experiment":
        if not stopped:
            number_of_generations.append(generations)
            evaluations.append(generations * (popsize / 2))
            generation_successful = False
        return evaluations, number_of_generations, generation_successful
    return False


def update_popsize(popsize, lower_bound_popsize, upper_bound_popsize, optimum_found):
    if optimum_found:
        new_popsize = int((popsize + lower_bound_popsize) / 2)
        if new_popsize % 10 == 0:
            return new_popsize, lower_bound_popsize, popsize, False
        else:
            return popsize, lower_bound_popsize, upper_bound_popsize, True

    else:
        if upper_bound_popsize is None:
            if popsize < 1280:
                return popsize * 2, popsize, None, False
            return 1280, 1280, 1280, True
        else:
            new_popsize = int((popsize + upper_bound_popsize) / 2)
            if new_popsize % 10 == 0:
                return new_popsize, popsize, upper_bound_popsize, False
            else:
                return upper_bound_popsize, lower_bound_popsize, upper_bound_popsize, True


def find_popsize(fitness_function, xover):
    popsize_found = False
    popsize = 10
    upper_bound_popsize = None
    lower_bound_popsize = None
    lives = 3

    while not popsize_found:
        optimum_found = False

        for j in range(50):
            optimum_found = run_generations(xover, fitness_function, popsize, "")

            if not optimum_found:
                lives -= 1

            if lives == 0:
                break

        (popsize, lower_bound_popsize, upper_bound_popsize, popsize_found) = update_popsize(popsize,
                                                                                            lower_bound_popsize,
                                                                                            upper_bound_popsize,
                                                                                            optimum_found)
        lives = 3
    print("popsize found: ", popsize)
    return popsize


def run_experiment(ff, xover):
    popsize = find_popsize(ff, xover)

    cpu_times = []
    evaluations = []
    amt_generations = []
    unsuccessful_generations = []
    t1 = process_time()
    for i in range(datapoints):
        (evals, amount_of_generations, generation_succesful) = run_generations(xover, ff, popsize, "experiment")
        if not generation_succesful:
            unsuccessful_generations.append(i)

        evaluations += evals
        amt_generations += amount_of_generations

    t2 = process_time()
    print("experiment finished")
    print("generations: ", amt_generations)
    print("unsuccesful generations: ", unsuccessful_generations)
    print("average amount of generations: ", mean(amt_generations))
    print("standard deviation of generations: ", stdev(amt_generations))

    print("processing time (s): ", t1 - t2)
    log_exp([ff.__name__,
             xover.__name__,
             popsize,
             mean(amt_generations), stdev(amt_generations), len(unsuccessful_generations),
             mean(evaluations), stdev(evaluations),
             t1 - t2,
             params.deceptiveness])


def __main__(x=None, fitfunc=None, crossover=None, assignment=None):
    ffs = [counting_ones, trap_function_linked, trap_function_non_linked]
    xovers = [uniform_crossover, two_point_crossover]

    if fitfunc == "plot":
        read_file()
        exit()

    if assignment is not None:
        print("running assignment ", assignment)
        for x in xovers:
            optimum_found = run_generations(x, counting_ones, population_size, assignment)
            print("optimum_found: ", optimum_found)

    else:
        if fitfunc is not None and crossover is not None:
            ffs = [ffs[int(fitfunc)]]
            xovers = [xovers[int(crossover)]]

        for ff in ffs:
            for xover in xovers:

                if ff.__name__ is "counting_ones":
                    print("\n\nrunning %s with %s" % (ff.__name__, xover.__name__))
                    run_experiment(ff, xover)
                else:
                    for d in [1, 2.5]:
                        print("\n\nrunning %s with %s and deceptiveness %s" % (ff.__name__, xover.__name__, d))
                        params.deceptiveness = d
                        run_experiment(ff, xover)


__main__(*argv)
