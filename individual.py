from params import deceptiveness, k_length


def counting_ones(gen):
    return sum(gen)


class Individual:
    def __init__(self, gen):
        self.genotype = gen  # list of numbers: 1 and 0
        self.fitness = 0

    def trap(self, n, k, d):
        if len(n) > 4:
            raise ValueError("Wrong input!!")
        ones = counting_ones(n)
        if k is ones:
            # print("k is ones")
            return k
        else:
            # print("ones", ones)
            b = k - d - ((k - d) / (k - 1)) * ones
            # print("b", b)
            return b

    def trap_function_linked(self, d, k):
        # lower d = more deceptive
        bees = []
        for j in range(int(len(self.genotype) / k)):
            # print(k + j)
            # print(self.genotype[j*k:j*k+k])
            bees.append(self.trap(self.genotype[j * k:j * k + k], k, d))
        return sum(bees)

    def trap_function_non_linked(self, d, k):
        # lower d = more deceptive
        bees = []
        gen_len = len(self.genotype)
        for i in range(int(gen_len / 4)):
            n = [self.genotype[i],
                 self.genotype[i + int(gen_len / 4)],
                 self.genotype[i + int(gen_len / 4) * 2],
                 self.genotype[i + int(gen_len / 4) * 3]]
            bees.append(self.trap(n, k, d))

        return sum(bees)

    def view_individual(self):
        print(self.genotype)
        print("ones: ", counting_ones(self.genotype))
        print("linked_trap: ", self.trap_function_linked(deceptiveness, k_length))
        print("nonlinked trap: ", self.trap_function_non_linked(deceptiveness, k_length))
