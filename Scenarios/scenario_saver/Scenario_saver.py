import os
from Scenarios.metrics import RMSE, MAE
import matplotlib.pyplot as plt

from Scenarios.scenario_saver.error_calulation import save_error
from Scenarios.scenario_saver.repair_saver import save_repair


def save_precision(repaired_scenario , path , repair_plot ):

    path = f"{path}/precision/"
    try:
        os.makedirs(path)
    except:
        pass

    save_error(repaired_scenario, path)
    if repair_plot:
        repair_path = path + "repair"
        try:
            os.makedirs(repair_path)
        except:
            pass
        repaired_scenario.save_repair_plots(repair_path)



save_folder = "Results"
def save_scenario(scenario ,repair_plot = False , res_name = None):
    scenario_name = scenario.scen_name
    data_name = scenario.data_name
    anomaly_type = scenario.a_type

    if res_name is not None:
        path = f"{save_folder}/{res_name}/{scenario_name}/{anomaly_type}/{data_name}"
    else:
        path = f"{save_folder}/{scenario_name}/{anomaly_type}/{data_name}"

    try:
        os.makedirs(path)
    except:
        pass

    save_precision(scenario,path,repair_plot = repair_plot)







