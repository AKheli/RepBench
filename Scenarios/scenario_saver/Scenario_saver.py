import os
from Scenarios.metrics import RMSE, MAE
import matplotlib.pyplot as plt

from Scenarios.scenario_saver.error_calulation import save_error
from Scenarios.scenario_saver.repair_saver import save_repair
from Scenarios.scenario_saver.run_time import save_runtime
from Scenarios.scenario_types.BaseScenario import BaseScenario

save_folder = "Results"



def save_precision(repaired_scenario , path , repair_plot ):

    path = f"{path}/precision/"
    try:
        os.makedirs(path)
    except:
        pass

    save_error(repaired_scenario, path)
    if repair_plot:
        save_repair(repaired_scenario,path )




def save_scenario(scenario ,repair_plot = False):
    scenario_name = scenario.scen_name
    data_name = scenario.data_name
    anomaly_type = scenario.a_type

    path = f"{save_folder}/{scenario_name}/{anomaly_type}/{data_name}"
    try:
        os.makedirs(path)
    except:
        pass

    save_precision(scenario,path,repair_plot = repair_plot)
    save_runtime(scenario,path)







