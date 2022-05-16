import os

from matplotlib import pyplot as plt

from Scenarios.scenario_saver.plotters import algo_plot, algo_plot_faster
from Scenarios.senario_methods import scenario_algos_figs


def save_repair(scenario , path):
    path = f"{path}/repair"
    try:
        os.makedirs(path)
    except:
        pass

    scenario_algos_figs(scenario, path)
    # for fig , algo in fig_generator:
    #     fig.savefig(f"{path}/{algo}.svg")
    # plt.close('all')
