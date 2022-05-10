import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import  run_ressources.Logger as log
from Scenarios.scenario_saver.plotters import generate_truth_and_injected, generate_repair_plot, \
    generate_correlated_series_plot
from Scenarios.scenario_types.BaseScenario import BaseScenario

import os

def generate_error_df_and_error_tables(scenario: BaseScenario, error_func):
    df = pd.DataFrame()
    repairs = scenario.repairs
    columns = scenario.injected_columns

    for scenario_part_name, v in scenario.scenarios.items():
        truth = v.get("truth", None) if v.get("truth", None) is not None else v.get("original", None)
        assert truth is not None
        injected = v["injected"]


        original_error = error_func(truth, injected, columns)
        if original_error == 0:
            if log.do_log:
                log.add_to_log( f"original error is 0 in  {scenario_part_name} ,{scenario.data_name} ")
                continue # todo check this

        assert original_error != 0 , f"original error is 0 in  {scenario_part_name} ,{scenario.data_name} "
        errors = {}#"original_error": (error_func(truth, injected, columns), "")}

        for algo_name, algo_output in repairs[scenario_part_name].items():
            error = error_func(truth, algo_output["repair"], columns, algo_output.get("labels", None))/original_error
            errors[algo_output["type"]] = (error, algo_output["name"])

        df = df.append(pd.Series(errors, name=scenario_part_name))
        error_df = df.applymap(lambda x: x[0])

    error_tables = {}

    for alg_type in df.columns:
        df_colum = df[alg_type]
        error_tables[alg_type] = pd.DataFrame(df_colum.tolist(), index=df.index, columns=["error", "algorithm"])

    return error_df, error_tables


def scenario_algos_figs(scenario: BaseScenario, path ,rasterize=True):
    algos = scenario.repair_names
    scenario_parts = scenario.scenarios
    plots_n = len(scenario_parts.keys())
    plot_height = 7
    total_height = plot_height * plots_n
    cols = scenario.injected_columns

    scenario_repairs = scenario.repairs

    for algo in algos:
        algo_path = f'{path}/{algo}'
        try:
            os.mkdir(algo_path)
        except:
            pass
        print(algos)
        plt.close('all')
        #fig, axs = plt.subplots(plots_n, figsize=(20, total_height), constrained_layout=True)
        # if rasterize:
        #     for ax in axs:
        #         ax.set_rasterization_zorder(0)

        part_list = list(scenario_parts.items())
        for i, (scenario_part_name, scenario_part_data) in enumerate(list(scenario_parts.items())):
            axis = plt.gca() #axs if plots_n == 1 else axs[i]
            axis.set_rasterization_zorder(0)
            axis.set_title(scenario_part_name)
            truth = scenario_part_data["original"]
            injected = scenario_part_data["injected"]
            class_ = scenario_part_data["class"]
            repair_df = scenario_repairs[scenario_part_name][algo]["repair"]
            algo_name = scenario_repairs[scenario_part_name][algo]["name"]
            axis.set_xlim(truth.index[0] - 0.1, truth.index[-1] + 0.1)

            line, = plt.plot(truth.iloc[:, cols[0]])
            lw = plt.getp(line, 'linewidth')

            #generate_correlated_series_plot(truth, cols, lw, axis)
            axis.set_prop_cycle(None)
            generate_repair_plot(repair_df, cols, algo, lw, axis)
            generate_truth_and_injected(truth, injected, cols, class_, lw, axis)
            axis.xaxis.set_major_locator(MaxNLocator(integer=True))

            #fig.suptitle(f'{scenario.data_name} ,{algo_name}' , size=22)

            plt.savefig(f"{algo_path}/{scenario_part_name}.svg")
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
