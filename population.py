from statistics import mean

import random

from individual import Individual
from params import genotype_size


class Population:
    def __init__(self):
        self.population = []
        self.fitness = None
        self.best = None

    def set_fitness(self):
        self.fitness = mean([i.fitness for i in self.population])
        self.best = max(self.population, key=lambda x: x.fitness)


def create_initial_population(popsize, ff):
    result = []
    for i in range(popsize):
        gen = random.choices([0, 1], k=genotype_size)
        individual = Individual(gen, ff)
        result += [individual]
    return result
