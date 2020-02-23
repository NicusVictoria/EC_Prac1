import csv

from params import generations


def log_exp(data):
    keys = ["fitness_function",
            "xover",
            "minimal_pop_size",
            "avg_amount_of_generations", "sdev_generations", "unsuccessful generations",
            "ff_evals", "sdev_ff_evals",
            "cpu_time",
            "deceptiveness"]
    datadict = dict(zip(keys, data))
    write_line(datadict, keys, "outputfile2_%sg.csv" % generations)


def write_line(dict, keys, filename):
    with open(filename, mode='a', newline='\n') as f:
        result_file = csv.DictWriter(f, fieldnames=keys)
        if f.tell() == 0:
            result_file.writeheader()

        result_file.writerow(dict)


def log1(data):
    keys = ["xover", "t", "prop"]
    datadict = dict(zip(keys, data))
    write_line(datadict, keys, "output_e1.csv")


def log2(data):
    keys = ["xover", "t", "errors", "corrects"]
    datadict = dict(zip(keys, data))
    write_line(datadict, keys, "output_e2.csv")


def log3(data):
    keys = ["xover", "t",
            "count_s0", "count_s1",
            "avg_fitness_s0", "stdev_fitness_s0",
            "avg_fitness_s1", "stdev_fitness_s1"]
    datadict = dict(zip(keys, data))
    write_line(datadict, keys, "output_e3.csv")
