from csv import reader

from matplotlib import pyplot


def read_file():
    ux = []
    tpx = []
    for [xover, t, prop] in reader(open('output_e1.csv')):
        if xover == "xover":
            continue
        elif xover == "uniform_crossover":
            ux.append(float(prop))
        else:
            tpx.append(float(prop))

    ux_plot = pyplot.plot(range(len(ux)), ux, label="uniform crossover")
    tpx_plot = pyplot.plot(range(len(tpx)), tpx, label="two-point clossover")

    pyplot.title("Proportions of 1-bit")
    pyplot.xlabel("Generations")
    pyplot.ylabel("Proportion of 1-bits")
    pyplot.legend()

    pyplot.show()
