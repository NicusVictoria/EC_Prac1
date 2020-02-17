import random

import numpy

from individual import Individual
from params import population_size, genotype_size


class Population:
    def __init__(self):
        self.population = []
        self.fitness = None

    def set_fitness(self):
        self.fitness = numpy.mean([i.fitness for i in self.population])


def create_initial_population():
    result = []
    for i in range(population_size):
        gen = random.choices([0, 1], k=genotype_size)
        individual = Individual(gen)
        result += [individual]
    return result
