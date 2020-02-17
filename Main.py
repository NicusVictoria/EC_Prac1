import random

from Crossover import uniform_crossover, compete
from params import generations
from population import Population, create_initial_population


def generation(p, g):
    random.shuffle(p.population)
    new_population = Population()

    for i in range(0, len(p.population), 2):
        children = uniform_crossover(p.population[i], p.population[i + 1], g)
        best = compete([p.population[i], p.population[i + 1], children[0], children[1]])
        new_population.population += best

    new_population.set_fitness()
    return new_population


def __main__():
    # Initial Population
    population = Population()
    population.population = create_initial_population()
    population.set_fitness()

    for i in range(generations):
        p = generation(population, i)
        print(p.fitness)
        if p.fitness == 100:
            print("Optimum reached in %s generations" % i)
            break
        population = p


__main__()
