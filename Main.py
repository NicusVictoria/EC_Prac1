from statistics import mean, stdev
from sys import argv
from time import process_time

import random

import params
from Crossover import uniform_crossover, two_point_crossover, compete
from individual import trap_function_non_linked, trap_function_linked, counting_ones
from params import generations
from population import Population, create_initial_population
from printer import write_line


def create_next_generation(p, g, xover, ff):
    random.shuffle(p.population)
    new_population = Population()
    updated = False

    for i in range(0, len(p.population), 2):
        children = xover(p.population[i], p.population[i + 1], g, ff)
        best, update = compete([p.population[i], p.population[i + 1], children[0], children[1]])
        updated = updated or update
        new_population.population += best

    new_population.set_fitness()
    return new_population, updated


def run_generations(xover, ff, popsize):
    pop = Population()
    pop.population = create_initial_population(popsize, ff)
    pop.set_fitness()
    for i in range(generations):

        p, updated = create_next_generation(pop, i, xover, ff)
        # print(p.best.fitness)
        if p.best.fitness == 100:
            # print("optimum found")
            return True
        if not updated:
            print("optimization unsuccesful")
            return False
        pop = p
    return False


def get_popsize(popsize, lower_bound_popsize, upper_bound_popsize, optimum_found):
    # returns (popsize, lowerbound, upperbound, popsize_found)
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
    lives = 2
    optimum_found = False

    while not popsize_found:
        optimum_found = False

        for j in range(25):
            # print("popsize ", popsize)

            optimum_found = run_generations(xover, fitness_function, popsize)

            if not optimum_found:
                lives -= 1

            if lives == 0:
                break

        (popsize, lower_bound_popsize, upper_bound_popsize, popsize_found) = get_popsize(popsize,
                                                                                         lower_bound_popsize,
                                                                                         upper_bound_popsize,
                                                                                         optimum_found)
        lives = 2
    print("popsize found: ", popsize)
    return popsize


def gen(xover, ff, popsize):
    number_of_generations = []
    evaluations = []

    pop = Population()
    pop.population = create_initial_population(popsize, ff)
    pop.set_fitness()
    updated = False
    stopped = False
    for i in range(generations):
        p, update = create_next_generation(pop, i, xover, ff)
        updated = updated or update
        # print(p.best.fitness)
        if p.best.fitness == 100:
            number_of_generations.append(i)
            evaluations.append(i * (popsize / 2))
            # print("Optimum reached in %s generations with popsize %s" % (i, popsize))
            # p.best.view_individual()
            stopped = True
            break
        if not updated:
            number_of_generations.append(i)
            evaluations.append(i * (popsize / 2))
            print("optimization unsuccessful")
            stopped = True
            break

        pop = p
    if not stopped:
        number_of_generations.append(generations)
        evaluations.append(generations * (popsize / 2))
    return evaluations, number_of_generations


def run_experiment(ff, xover):
    popsize = find_popsize(ff, xover)

    cpu_times = []
    evaluations = []
    amt_generations = []

    for i in range(25):
        t1 = process_time()
        (evals, amount_of_generations) = gen(xover, ff, popsize)
        evaluations += evals
        amt_generations += amount_of_generations
        t2 = process_time()
        cpu_times.append(t2 - t1)
    print("experiment finished")
    print("average amount of generations: ", mean(amt_generations))
    print("average amount of processing time (s): ", mean(cpu_times))
    write_line([ff.__name__, xover.__name__, popsize, mean(amt_generations), stdev(amt_generations),
                mean(evaluations),
                stdev(evaluations), mean(cpu_times), stdev(cpu_times), params.deceptiveness])


def __main__(x=None, a=None, b=None):
    ffs = [counting_ones, trap_function_linked, trap_function_non_linked]
    xovers = [uniform_crossover, two_point_crossover]
    if a is not None and b is not None:
        ffs = [ffs[int(a)]]
        xovers = [xovers[int(b)]]

    for ff in ffs:
        for xover in xovers:

            if ff.__name__ is "counting_ones":
                print("running %s with %s" % (ff.__name__, xover.__name__))
                run_experiment(ff, xover)
            else:
                for d in [1, 2.5]:
                    print("running %s with %s and deceptiveness %s" % (ff.__name__, xover.__name__, d))
                    params.deceptiveness = d
                    run_experiment(ff, xover)


__main__(*argv)
