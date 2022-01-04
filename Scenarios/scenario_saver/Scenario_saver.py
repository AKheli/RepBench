import os
from Scenarios.metrics import RMSE, MAE
import matplotlib.pyplot as plt

from Scenarios.scenario_saver.error_calulation import generate_error_df, save_error
from Scenarios.scenario_saver.repair_saver import save_repair
from Scenarios.scenario_saver.run_time import save_runtime

save_folder = "Results"



def save_precision(repaired_scenario_dict , path):

    path = f"{path}/precision/"
    try:
        os.makedirs(path)
    except:
        pass

    save_error(repaired_scenario_dict, path)
    save_repair(repaired_scenario_dict,path)




def save_scenario(repaired_scenario_dict):
    scenario_type = repaired_scenario_dict["scenario_type"]
    scenario_name = scenario_type.scenario_type
    data_name = repaired_scenario_dict["data_name"]

    path = f"{save_folder}/{scenario_name}/{scenario_type.anomaly_type}/{data_name}"
    try:
        os.makedirs(path)
    except:
        pass

    save_precision(repaired_scenario_dict,path)
    save_runtime(repaired_scenario_dict,path)







