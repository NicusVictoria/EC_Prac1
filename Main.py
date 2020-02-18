import random

from Crossover import uniform_crossover, two_point_crossover, compete
from params import generations
from population import Population, create_initial_population
from individual import counting_ones


def generation(p, g, xover, ff):
    random.shuffle(p.population)
    new_population = Population()

    for i in range(0, len(p.population), 2):
        children = xover(p.population[i], p.population[i + 1], g, ff)
        best = compete([p.population[i], p.population[i + 1], children[0], children[1]])
        new_population.population += best

    new_population.set_fitness()
    return new_population


def run_generations(xover, ff, pop):
    for i in range(generations):

        p = generation(pop, i, xover, ff)
        # print(p.best.fitness)
        if p.best.fitness == 100:
            print("optimum found")
            return True
        pop = p
    return False


def get_popsize(popsize, lower_bound_popsize, upper_bound_popsize, optimum_found):
    # returns (popsize, lowerbound, upperbound, popsize_found)
    if optimum_found:
        new_popsize = popsize + lower_bound_popsize / 2
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
            new_popsize = popsize + upper_bound_popsize / 2
            if new_popsize % 10 == 0:
                return popsize + upper_bound_popsize / 2, popsize, upper_bound_popsize, False
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
            print("popsize ", popsize)

            population = Population()
            population.population = create_initial_population(10, fitness_function)
            population.set_fitness()

            optimum_found = run_generations(xover, fitness_function, population)

            if not optimum_found:
                lives -= 1

            if lives == 0:
                (popsize, lower_bound_popsize, upper_bound_popsize, popsize_found) = get_popsize(popsize,
                                                                                                 lower_bound_popsize,
                                                                                                 upper_bound_popsize,
                                                                                                 optimum_found)
                lives = 2

            if popsize_found:
                return popsize

        (popsize, lower_bound_popsize, upper_bound_popsize, popsize_found) = get_popsize(popsize,
                                                                                         lower_bound_popsize,
                                                                                         upper_bound_popsize,
                                                                                         optimum_found)


def __main__():
    ff = counting_ones
    xover = uniform_crossover
    # Initial Population
    popsize = 40#find_popsize(ff, xover)
    population = Population()
    population.population = create_initial_population(popsize, ff)
    population.set_fitness()

    for i in range(generations):
        p = generation(population, i, xover, ff)
        print(p.best.fitness)
        if p.best.fitness == 100:
            print("Optimum reached in %s generations with popsize %s" % (i, popsize))
            p.best.view_individual()
            break
        population = p


__main__()
