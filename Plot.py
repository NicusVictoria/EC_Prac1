from csv import reader

from matplotlib import pyplot


def read_file(e):
    if e == 'e1':
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

    elif e == 'e2':
        ux_error = []
        ux_correct = []
        tpx_error = []
        tpx_correct = []

        for [xover, t, errors, corrects] in reader(open('output_e2.csv')):
            if xover == "xover":
                continue
            elif xover == "uniform_crossover":
                ux_error.append(float(errors))
                ux_correct.append(float(corrects))
            else:
                tpx_error.append(float(errors))
                tpx_correct.append(float(corrects))

        # ux_plot_e = pyplot.plot(range(len(ux_error)), ux_error, label="error selections")
        # ux_plot_c = pyplot.plot(range(len(ux_correct)), ux_correct, label="correct selections")
        #
        # pyplot.title("Error selections uniform crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("Selections")
        # pyplot.legend()
        #
        # pyplot.show()

        tpx_plot_e = pyplot.plot(range(len(tpx_error)), tpx_error, label="error selections")
        tpx_plot_c = pyplot.plot(range(len(tpx_correct)), tpx_correct, label="correct selections")

        pyplot.title("Error selections two_point crossover")
        pyplot.xlabel("Generations")
        pyplot.ylabel("Selections")
        pyplot.legend()

        pyplot.show()

    else:
        ux_sols0 = []
        ux_sols1 = []
        ux_fit0 = []
        ux_fit1 = []
        ux_sdev0 = []
        ux_sdev1 = []

        tpx_sols0 = []
        tpx_sols1 = []
        tpx_fit0 = []
        tpx_fit1 = []
        tpx_sdev0 = []
        tpx_sdev1 = []

        for [xover, t,
             count_s0, count_s1,
             avg_fitness_s0, stdev_fitness_s0,
             avg_fitness_s1, stdev_fitness_s1] \
                in reader(open('output_e3.csv')):
            if xover == "xover":
                continue
            elif xover == "uniform_crossover":
                ux_sols0.append(float(count_s0))
                ux_sols1.append(float(count_s1))
                try:
                    ux_fit0.append(float(avg_fitness_s0))
                except:
                    pass
                ux_fit1.append(float(avg_fitness_s1))
                ux_sdev0.append(float(stdev_fitness_s0))
                ux_sdev1.append(float(stdev_fitness_s1))
            else:
                tpx_sols0.append(float(count_s0))
                tpx_sols1.append(float(count_s1))
                try:
                    tpx_fit0.append(float(avg_fitness_s0))
                except:
                    pass
                tpx_fit1.append(float(avg_fitness_s1))
                tpx_sdev0.append(float(stdev_fitness_s0))
                tpx_sdev1.append(float(stdev_fitness_s1))

        # pyplot.plot(range(len(ux_sols0)), ux_sols0, label="schema 0")
        # pyplot.plot(range(len(ux_sols1)), ux_sols1, label="schema 1")
        # 
        # pyplot.title("Schemata count uniform crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("count")
        # pyplot.legend()
        # pyplot.show()

        pyplot.plot(range(len(tpx_sols0)), tpx_sols0, label="schema 0")
        pyplot.plot(range(len(tpx_sols1)), tpx_sols1, label="schema 1")

        pyplot.title("Schemata count two_point crossover")
        pyplot.xlabel("Generations")
        pyplot.ylabel("count")
        pyplot.legend()
        pyplot.show()

        # pyplot.plot(range(len(ux_fit0)), ux_fit0, 'k')
        # pyplot.fill_between(range(len(ux_fit0)),
        #                     [ux_fit0[i] - ux_sdev0[i] for i in range(len(ux_fit0))],
        #                     [ux_fit0[i] + ux_sdev0[i] for i in range(len(ux_fit0))])
        # pyplot.title("Schemata-0 uniform crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("Schema fitness")
        # pyplot.show()

        # pyplot.plot(range(len(ux_fit1)), ux_fit1, 'k')
        # pyplot.fill_between(range(len(ux_fit1)),
        #                     [ux_fit1[i] - ux_sdev1[i] for i in range(len(ux_fit1))],
        #                     [ux_fit1[i] + ux_sdev1[i] for i in range(len(ux_fit1))])
        # pyplot.title("Schemata-1 uniform crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("Schema fitness")
        # pyplot.show()

        # pyplot.plot(range(len(tpx_fit0)), tpx_fit0, 'k')
        # pyplot.fill_between(range(len(tpx_fit0)),
        #                     [tpx_fit0[i] - tpx_sdev0[i] for i in range(len(tpx_fit0))],
        #                     [tpx_fit0[i] + tpx_sdev0[i] for i in range(len(tpx_fit0))])
        # pyplot.title("Schemata-0 two-point crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("Schema fitness")
        # pyplot.show()

        # pyplot.plot(range(len(tpx_fit1)), tpx_fit1, 'k')
        # pyplot.fill_between(range(len(tpx_fit1)),
        #                     [tpx_fit1[i] - tpx_sdev1[i] for i in range(len(tpx_fit1))],
        #                     [tpx_fit1[i] + tpx_sdev1[i] for i in range(len(tpx_fit1))])
        # pyplot.title("Schemata-1 two-point crossover")
        # pyplot.xlabel("Generations")
        # pyplot.ylabel("Schema fitness")
        # pyplot.show()
