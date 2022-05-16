import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import  run_ressources.Logger as log
from Scenarios.data_part import DataPart
from Scenarios.scenario_saver.plotters import generate_truth_and_injected, generate_repair_plot, \
    generate_correlated_series_plot

import os


def scenario_algos_figs(scenario, path ,rasterize=True):
    algos = scenario.repair_names
    scenario_parts = scenario.part_scenarios
    plots_n = len(scenario_parts.keys())
    plot_height = 7
    total_height = plot_height * plots_n

    for algo in algos:
        algo_path = f'{path}/{algo}'
        try:
            os.mkdir(algo_path)
        except:
            pass
        plt.close('all')
        #fig, axs = plt.subplots(plots_n, figsize=(20, total_height), constrained_layout=True)
        # if rasterize:
        #     for ax in axs:
        #         ax.set_rasterization_zorder(0)

        for  name ,_ , test  ,  in scenario.name_train_test_iter:
            scenario_part : DataPart = test
            axis = plt.gca() #axs if plots_n == 1 else axs[i]
            axis.set_rasterization_zorder(0)
            axis.set_title(name)

            cols = scenario_part.injected_columns
            truth = scenario_part.truth
            injected = scenario_part.injected
            class_ = scenario_part.klass

            assert algo in scenario_part.repairs , f"{algo} not in {scenario_part.repairs.keys()}"
            algo_part = scenario_part.repairs[algo]

            repair_df = algo_part["repair"]
            algo_name = algo_part["name"]
            axis.set_xlim(truth.index[0] - 0.1, truth.index[-1] + 0.1)

            line, = plt.plot(truth.iloc[:, cols[0]])
            lw = plt.getp(line, 'linewidth')

            #generate_correlated_series_plot(truth, cols, lw, axis)
            axis.set_prop_cycle(None)
            generate_repair_plot(repair_df, cols, algo, lw, axis)
            generate_truth_and_injected(truth, injected, cols, class_, lw, axis)
            axis.xaxis.set_major_locator(MaxNLocator(integer=True))

            #fig.suptitle(f'{scenario.data_name} ,{algo_name}' , size=22)

            plt.savefig(f"{algo_path}/{name}.svg")
            plt.close('all')

# def repair_scenario(injected_scenario : BaseScenario, repair_algos):
#
#     params = {}
#     params["train"] = injected_scenario.train
#     params["train_class"] = injected_scenario.train["class"]
#
#     part_scenarios = injected_scenario.scenarios
#
#     for name ,values  in part_scenarios.items():
#         params["truth"] = values["original"]
#         params["injected"] = values["injected"]
#         params["cols"] = values["columns"]
#
#         for algo_info in repair_algos:
#             print("info" , algo_info)
#             pre_params = algo_info["params"]
#             pre_params.update(params)
#             result = algo_info["algorithm"](**pre_params)
#             injected_scenario.add_repair(name,result , result["name"])
#         # with Pool() as pool:
#         #     results = list(map(f, repair_algos))
#         #     for repair in results:
#         #         repairs[repair["name"]] = repair
#         #
#         # part_scenarios[scenario_part_name]["repairs"] = repairs
#     return injected_scenario
#
#
