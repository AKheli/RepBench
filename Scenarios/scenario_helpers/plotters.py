import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import figure

def scenario_plot(scenario_data, path):

    for scenario_part_name, scenario_part_data in scenario_data.items():
        scenario_part_plot(scenario_part_name,scenario_part_data, path)

def scenario_part_plot(scenario_part_name, scenario_part , path):
    truth = scenario_part["original"]
    injected = scenario_part["injected"]
    cols = scenario_part["columns"]
    repairs = scenario_part["repairs"]


    ## full plot
    figure(figsize=(20, 7))
    line, = plt.plot(truth.iloc[:, cols[0]])
    lw = plt.getp(line, 'linewidth')

    generate_correlated_series_plot(truth, cols , lw)
    for algo_name , repair_output in repairs.items():
        repair_df = repair_output["repair"]
        generate_repair_plot(repair_df, cols,algo_name, lw )
        plt.title(algo_name)

    generate_truth_and_injected(truth, injected, cols, lw)
    plt.legend()
    plt.savefig(f"{path}/all_algos.svg")# ,dpi=300)
    plt.close()


    ## indivual plots
    line, = plt.plot(truth.iloc[:, cols[0]])
    lw = plt.getp(line, 'linewidth')
    for algo_name, repair_output in repairs.items():
        figure(figsize=(20, 7))
        generate_correlated_series_plot(truth, cols, lw)
        plt.xlim((truth.index[0]-2, truth.index[-1]+2))
        repair_df = repair_output["repair"]
        generate_repair_plot(repair_df, cols,algo_name, lw)
        plt.title(algo_name)
        generate_truth_and_injected(truth, injected, cols, lw)
        plt.savefig(f"{path}/{algo_name}.svg")#, dpi=300)
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


def generate_correlated_series_plot(truth, cols , lw ,  ax = plt):
    for i, column in enumerate(truth.columns):
        alpha = 0.1
        if i not in cols:
            ax.plot(truth[column], alpha=alpha, lw=lw / 3)
    plt.gca().set_prop_cycle(None)

def generate_truth_and_injected(truth,injected, cols, lw , ax = plt):
    for i, column in enumerate(truth.columns):
        if i in cols:
            ax.plot(injected[column], color="red", lw=lw / 2, ls= "dotted" , label = "injected")
            ax.plot(truth[column], color="black", lw=lw , label = "truth")


def generate_repair_plot(repair_df, cols , algo_name,lw, ax = plt):
       for i, column in enumerate(repair_df.columns):
            if i in cols:
                ax.plot(repair_df[column], lw=lw/2,label=algo_name)


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

