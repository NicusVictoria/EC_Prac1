import random
from individual import Individual
from params import genotype_size, population_size


def generation(population):
    p = random.shuffle(population, random.random())
    # pairs
    # offspring
    # family competition


def create_population(size):
    gen = random.choices([0, 1], k=genotype_size)
    individual = Individual(gen)
    return [individual]


def __main__():
    population = create_population(population_size)
    population[0].view_individual()


__main__()
