import os
from Scenarios.metrics import RMSE, MAE
import matplotlib.pyplot as plt

from Scenarios.scenario_saver.error_calulation import generate_error_df, save_error
from Scenarios.scenario_saver.repair_saver import save_repair
from Scenarios.scenario_saver.run_time import save_runtime
from Scenarios.scenario_types.BaseScenario import BaseScenario

save_folder = "Results"



def save_precision(repaired_scenario , path):

    path = f"{path}/precision/"
    try:
        os.makedirs(path)
    except:
        pass

    save_error(repaired_scenario, path)
    save_repair(repaired_scenario,path)




def save_scenario(repaired_scenario : BaseScenario):
    scenario_name = repaired_scenario.scenario_type
    data_name = repaired_scenario.data_name
    anomaly_type = repaired_scenario.anomaly_type

    path = f"{save_folder}/{scenario_name}/{anomaly_type}/{data_name}"
    try:
        os.makedirs(path)
    except:
        pass

    save_precision(repaired_scenario,path)
    #save_runtime(repaired_scenario,path)






