from statistics import mean, stdev
from sys import argv
from time import process_time

import random

import params
from Crossover import uniform_crossover, two_point_crossover, compete
from individual import trap_function_non_linked, trap_function_linked, counting_ones
from params import generations, datapoints
from population import Population, create_initial_population
from printer import write_line


def create_next_generation(p, xover, ff):
    random.shuffle(p.population)
    new_population = Population()
    updated = False

    for i in range(0, len(p.population), 2):
        parent1 = p.population[i]
        parent2 = p.population[i + 1]
        parent1.generation = "parent"
        parent2.generation = "parent"
        child1, child2 = xover(parent1, parent2, ff)
        best, update = compete([parent1, parent2, child1, child2])
        updated = updated or update
        new_population.population += best

    new_population.set_fitness()
    return new_population, updated


def run_generations(xover, ff, popsize, log):
    number_of_generations = []
    evaluations = []
    indexes_unsuccessful_generations = []

    pop = Population()
    pop.population = create_initial_population(popsize, ff)
    pop.set_fitness()

    stopped = False
    generation_successful = True

    for i in range(generations):

        p, updated = create_next_generation(pop, xover, ff)

        if p.best.fitness == 100:
            if log:
                number_of_generations.append(i)
                evaluations.append(i * (popsize / 2))
                stopped = True
                break
            return True
        if not updated:
            # print("optimization unsuccessful")
            if log:
                number_of_generations.append(i)
                evaluations.append(i * (popsize / 2))
                generation_successful = False
                stopped = True
                break
            return False
        pop = p
    if log:
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
            optimum_found = run_generations(xover, fitness_function, popsize, False)

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
        (evals, amount_of_generations, generation_succesful) = run_generations(xover, ff, popsize, True)
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
    write_line([ff.__name__,
                xover.__name__,
                popsize,
                mean(amt_generations), stdev(amt_generations), len(unsuccessful_generations),
                mean(evaluations), stdev(evaluations),
                t1 - t2,
                params.deceptiveness])


def __main__(x=None, a=None, b=None):
    ffs = [counting_ones, trap_function_linked, trap_function_non_linked]
    xovers = [uniform_crossover, two_point_crossover]
    if a is not None and b is not None:
        ffs = [ffs[int(a)]]
        xovers = [xovers[int(b)]]

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
