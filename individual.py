from params import deceptiveness, k_length


def counting_ones(gen):
    return sum(gen)


class Individual:
    def __init__(self, gen):
        self.genotype = gen  # list of numbers: 1 and 0
        self.fitness = self.counting_ones()
        self.generation = 0

    def counting_ones(self):
        return counting_ones(self.genotype)

    def trap(self, n):
        if len(n) > 4:
            raise ValueError("Wrong input!!")
        ones = counting_ones(n)
        if k_length is ones:
            return k_length
        else:
            b = k_length - deceptiveness - ((k_length - deceptiveness) / (k_length - 1)) * ones
            return b

    def trap_function_linked(self):
        # lower deceptiveness = more deceptive
        bees = []
        for j in range(int(len(self.genotype) / k_length)):
            bees.append(self.trap(self.genotype[j * k_length:j * k_length + k_length]))
        return sum(bees)

    def trap_function_non_linked(self):
        # lower deceptiveness = more deceptive
        bees = []
        gen_len = len(self.genotype)
        for i in range(int(gen_len / 4)):
            n = [self.genotype[i],
                 self.genotype[i + int(gen_len / 4)],
                 self.genotype[i + int(gen_len / 4) * 2],
                 self.genotype[i + int(gen_len / 4) * 3]]
            bees.append(self.trap(n))

        return sum(bees)

    def view_individual(self):
        print(self.genotype)
        print("ones: ", counting_ones(self.genotype))
        print("linked_trap: ", self.trap_function_linked())
        print("nonlinked trap: ", self.trap_function_non_linked())
