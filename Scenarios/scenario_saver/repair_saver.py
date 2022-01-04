import os

from Scenarios.scenario_saver.plotters import algo_plot, algo_plot_faster


def save_repair(repaired_scenario_dict, path):
    path = f"{path}/repair"
    try:
        os.makedirs(path)
    except:
        pass

    scenario_type = repaired_scenario_dict["scenario_type"]
    scenario_data = repaired_scenario_dict["scenario_data"]
    algo_plot(scenario_data, path, title=scenario_type.small_data_description)
