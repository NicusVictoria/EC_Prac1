import params
from params import k_length


def counting_ones(gen):
    return sum(gen)


def trap(n):
    if len(n) > 4:
        raise ValueError("Wrong input!!")
    ones = counting_ones(n)
    if k_length is ones:
        return k_length
    else:
        b = k_length - params.deceptiveness - ((k_length - params.deceptiveness) / (k_length - 1)) * ones
        return b


def trap_function_linked(genotype):
    bees = []
    for j in range(int(len(genotype) / k_length)):
        bees.append(trap(genotype[j * k_length:j * k_length + k_length]))
    return sum(bees)


def trap_function_non_linked(genotype):
    bees = []
    gen_len = len(genotype)
    for i in range(int(gen_len / 4)):
        n = [genotype[i],
             genotype[i + int(gen_len / 4)],
             genotype[i + int(gen_len / 4) * 2],
             genotype[i + int(gen_len / 4) * 3]]
        bees.append(trap(n))

    return sum(bees)


class Individual:
    def __init__(self, gen, fitness_function):
        self.genotype = gen  # list of numbers: 1 and 0
        self.fitness = fitness_function(gen)
        self.generation = "child"

    def view_individual(self):
        print(self.genotype)
        print("fitness: ", self.fitness)
        print("generation: ", self.generation)
