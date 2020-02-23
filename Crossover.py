import random

from individual import Individual


def uniform_crossover(parent1, parent2, ff):
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

    child1 = Individual(c1, ff)
    child2 = Individual(c2, ff)
    return child1, child2


def two_point_crossover(parent1, parent2, ff):
    if len(parent1.genotype) is not len(parent2.genotype):
        raise ValueError("Parents have different length!?")

    split1 = random.randint(0, len(parent1.genotype))
    split2 = random.randint(split1, len(parent1.genotype))

    child1 = Individual(parent2.genotype[0:split1] + parent1.genotype[split1:split2] + parent2.genotype[split2:], ff)
    child2 = Individual(parent1.genotype[0:split1] + parent2.genotype[split1:split2] + parent1.genotype[split2:], ff)
    return child1, child2


def printfamily(f):
    print("\n\nfamily")
    for i in f:
        i.view_individual()


def selection_error(parent1, parent2, win1, win2):
    error_counter = 0
    correct_counter = 0
    for i in range(len(parent1.genotype)):
        if parent1.genotype[i] != parent2.genotype[i]:
            if win1.genotype[i] == 0 and win2.genotype[i] == 0:
                error_counter += 1
            if win1.genotype[i] == 1 and win2.genotype[i] == 1:
                correct_counter += 1
    return error_counter, correct_counter


def compete(p1, p2, c1, c2):
    family = [p1, p2, c1, c2]
    family.sort(key=lambda x: (x.fitness, x.generation))
    updated = True
    if family[3].generation is "parent" and family[2].generation is "parent":
        updated = False
    error, correct = selection_error(p1, p2, family[3], family[2])
    return family[2:], updated, error, correct
