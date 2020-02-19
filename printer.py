import csv


def write_line(data):
    keys = ["fitness_function", "xover", "minimal_pop_size", "avg_amount_of_generations",
            "sdev_generations", "ff_evals", "sdev_ff_evals", "cpu_time", "sdev_cpu_time", "deceptiveness"]
    datadict = dict(zip(keys, data))
    print(datadict)

    with open("outputfile.csv", mode='a', newline='\n') as f:
        result_file = csv.DictWriter(f, fieldnames=keys)
        if f.tell() == 0:
            result_file.writeheader()

        result_file.writerow(datadict)
