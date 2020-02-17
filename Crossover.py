import random

from individual import Individual


def uniform_crossover(parent1, parent2, g):
    if len(parent1.genotype) is not len(parent2.genotype):
        raise ValueError("Parents have different length!?")
    c1 = []
    c2 = []
    for i in range(len(parent1.genotype)):
        n = random.random()
        if n < 0.5:
            c1.append(parent1.genotype[i])
            c2.append(parent2.genotype[i])
        else:
            c1.append(parent2.genotype[i])
            c2.append(parent1.genotype[i])

    child1 = Individual(c1)
    child1.generation = g + 1
    child2 = Individual(c2)
    child2.generation = g + 1
    return [child1, child2]


def two_point_crossover(parent1, parent2, g):
    if len(parent1.genotype) is not len(parent2.genotype):
        raise ValueError("Parents have different length!?")

    split1 = random.randint(0, len(parent1.genotype))
    split2 = random.randint(split1, len(parent1.genotype))

    child1 = Individual(parent2[0:split1] + parent1[split1:split2] + parent2[split2:])
    child1.generation = g + 1
    child2 = Individual(parent1[0:split1] + parent2[split1:split2] + parent1[split2:])
    child2.generation = g + 1
    return [child1, child2]


def compete(family):
    family.sort(key=lambda x: (x.fitness, x.generation))
    return family[:2]
