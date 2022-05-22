import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import figure
import numpy as np
from matplotlib.ticker import MaxNLocator

from Repair.res.timer import Timer
from Scenarios.scenario_saver.anomaly_split import split


def algo_plot_faster(scenario_data, path, title):
    matplotlib.use('Agg')
    algo_plot(scenario_data, path, title)


def algo_plot(scenario_data, path, title):
    timer = Timer()
    timer.start()
    algos = list(scenario_data.values())[0]["repairs"].keys()

    plots_n = len(scenario_data.keys())

    plot_height = 7
    total_height = plot_height * plots_n
    for algo in algos:
        plt.close('all')
        fig, axs = plt.subplots(plots_n, figsize=(20, total_height), constrained_layout=True)
        for i, (scenario_part_name, scenario_part_data) in enumerate(scenario_data.items()):
            if plots_n == 1:
                axis = axs
            else:
                axis = axs[i]

            axis.set_title(scenario_part_name)
            truth = scenario_part_data["original"]
            injected = scenario_part_data["injected"]
            cols = scenario_part_data["columns"]
            repair_df = scenario_part_data["repairs"][algo]["repair"]

            axis.set_xlim(truth.index[0] - 0.1, truth.index[-1] + 0.1)

            line, = plt.plot(truth.iloc[:, cols[0]])
            lw = plt.getp(line, 'linewidth')

            generate_correlated_series_plot(truth, cols, lw, axis)
            axis.set_prop_cycle(None)
            generate_repair_plot(repair_df, cols, algo, lw, axis)
            generate_truth_and_injected(truth, injected, cols, lw, axis)
            axis.xaxis.set_major_locator(MaxNLocator(integer=True))

        fig.suptitle(title, size=22)
        # fig.tight_layout(pad=2.0)
        # plt.subplots_adjust(top= 1-0.20/plots_n)
        timer2 = Timer()
        timer2.start()
        #print(fig.lines)
        fig.savefig(f"{path}/{algo}.svg")
        with open(f"{path}/{algo}.svg", "r") as f:
            list_of_lines = f.readlines()

        with open(f"{path}/{algo}.svg", "w") as f2:
            rounded = lambda x: f'L {round(float(x[1]))} {round(float(x[2]))}'
            f2.writelines([rounded(l.split()) if l.startswith("L") else l for l in list_of_lines])
        timer.start()

        print(timer2.get_time())

        # plot some anomalies
        plt.close()
        plt.clf()
        splits = split(truth, injected, 0)
        counter = 0
        for anomaly_range in splits[-min(3, len(splits)):]:
            counter += 1
            generate_correlated_series_plot(truth.iloc[anomaly_range, :], cols, lw)
            axis.set_prop_cycle(None)
            generate_repair_plot(repair_df.iloc[anomaly_range, :], cols, algo, lw)
            generate_truth_and_injected(truth.iloc[anomaly_range, :], injected.iloc[anomaly_range, :], cols, lw)

            plt.savefig(f"{path}/{algo}anom{counter}.svg", dpi=3)
            plt.savefig(f"{path}/{algo}anom{counter}.svg", dpi=3)

            plt.close()
            plt.clf()
        print(timer.get_time())


def scenario_plot(scenario_data, path):
    for scenario_part_name, scenario_part_data in scenario_data.items():
        scenario_part_plot(scenario_part_name, scenario_part_data, path)


def scenario_part_plot(scenario_part_name, scenario_part, path):
    truth = scenario_part["original"]
    injected = scenario_part["injected"]
    cols = scenario_part["columns"]
    repairs = scenario_part["repairs"]

    ## full plot
    figure(figsize=(20, 7))
    line, = plt.plot(truth.iloc[:, cols[0]])
    lw = plt.getp(line, 'linewidth')

    generate_correlated_series_plot(truth, cols, lw)
    for algo_name, repair_output in repairs.items():
        repair_df = repair_output["repair"]
        generate_repair_plot(repair_df, cols, algo_name, lw)
        plt.title(algo_name)

    generate_truth_and_injected(truth, injected, cols, lw)
    plt.legend()
    plt.savefig(f"{path}/all_algos.svg")  # ,dpi=300)
    plt.close()

    ## indivual plots
    line, = plt.plot(truth.iloc[:, cols[0]])
    lw = plt.getp(line, 'linewidth')
    for algo_name, repair_output in repairs.items():
        figure(figsize=(20, 7))

        generate_correlated_series_plot(truth, cols, lw)
        plt.xlim((truth.index[0] - 2, truth.index[-1] + 2))
        repair_df = repair_output["repair"]
        generate_repair_plot(repair_df, cols, algo_name, lw)
        plt.title(algo_name)
        generate_truth_and_injected(truth, injected, cols, lw)
        # plt.savefig(f"{path}/{algo_name}.svg")  # , dpi=300)
        plt.savefig(f"{path}/{algo_name}300.png", dpi=300)
        plt.savefig(f"{path}/{algo_name}.eps")  # , dpi=300)
        plt.savefig(f"{path}/{algo_name}300.eps", dpi=300)
        plt.savefig(f"{path}/{algo_name}1000.eps", dpi=1000)
        plt.savefig(f"{path}/{algo_name}1000.png", dpi=1000)

        plt.close()

    # fig, axs = plt.subplots(len(repairs.keys()) ,figsize=(20, 7*len(repairs.keys())) )
    #
    # axis_counter = 0
    # for algo_name, repair_output in repairs.items():
    #     axis = axs[axis_counter]
    #     axis.set_title(algo_name)
    #     generate_correlated_series_plot(truth, cols, lw ,axis)
    #     repair_df = repair_output["repair"]
    #     generate_repair_plot(repair_df, cols, lw,axis)
    #     generate_truth_and_injected(truth, injected, cols, lw,axis)
    #     #axis.title = algo_name
    #     axis_counter += 1
    # plt.savefig(f"{path}/algos.svg") #, dpi=300)
    # plt.close()


def generate_correlated_series_plot(truth, cols, lw, ax=plt):
    for i, column in enumerate(truth.columns):
        alpha = 0.1
        if i not in cols:
            ax.plot(truth[column], alpha=alpha, lw=lw / 3)
    plt.gca().set_prop_cycle(None)


def generate_truth_and_injected(truth, injected, cols,class_, lw, ax=plt , alpha = 1):
    class_ = np.array(class_)
    for i, column in enumerate(truth.columns):
        if i in cols:
            class_c = class_[:,i]
            mask = np.ma.masked_where(np.invert(class_c),injected[column])
            ax.plot(mask, color="red", ls='None',marker=".")
            extended_class = np.array([False]+[ class_c[i-1] or class_c[i] or class_c[i+1] for i in  np.arange(1,len(class_c)-1)]+[False])
            mask = np.ma.masked_where(np.invert(extended_class),injected[column])
            ax.plot(mask, color="red", lw=lw / 2, ls="dotted",marker=None, label="injected")
            #ax.scatter(injected[column], s=mask, marker='.',color="red")# , marker=".")
            ax.plot(truth[column], color="black", lw=lw, label  ="truth" , alpha=alpha)


def generate_bouneries_plot(lower, upper, lw, ax=plt):
    ax.plot(lower, color="green", lw=lw / 2, ls="dotted", label="lower")  # , marker=".")
    ax.plot(upper, color="green", lw=lw / 2, ls="dotted", label="upper")

def generate_line_plot(reduced,lw, ax=plt , color="brown"):
    ax.plot(reduced, color=color, lw=lw , ls="dashed", label="lower")  # , marker=".")

def generate_repair_plot(repair_df, cols, algo_name, lw, ax=plt):
    for i, column in enumerate(repair_df.columns):
        if i in cols:
            ax.plot(repair_df[column], lw=lw / 2, label=algo_name)

# def generate_repair_plot_anomalies(repair_df,truth, injected, cols,pdf):
#     plt.close()
#     for i,column in enumerate(repair_df.columns):
#         if cols is not None and i not in cols:
#             pass
#         else:
#             plt.plot(truth[column], color="black", )
#             plt.plot(injected[column], color="red")
#
#             plt.plot(repair_df[column])
#
#
