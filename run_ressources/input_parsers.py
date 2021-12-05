from Scenarios.Anomaly_Types import parse_anomaly_name
from Scenarios.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.Scenario_Types import parse_scenario_name
from data_methods.Helper_methods import searchfiles, display_data_folder
from Repair.repair_algos.Robust_PCA.PCA_algorithms import *
from Scenarios.BaseScenario import BaseScenario

def parse_data_argument(arg):
    try:
        filename_paths = searchfiles(arg)
        print(filename_paths , "paths")
    except ValueError as e:
        print("Data file not found or not given. \nData folder contains:")
        files = '\n'.join([name for name in display_data_folder() if not name.endswith('.py')])
        print(f"{files}")
        exit()
    return filename_paths

def parse_anomaly_argument(arg):
    return parse_anomaly_name(arg)


def get_scenario(scenario_name,anomaly_type , param_dict = None):
    name =  parse_scenario_name(scenario_name)
    if param_dict is None:
        return SCENARIO_CONSTRUCTORS[name](anomaly_type)
    else:
        return  SCENARIO_CONSTRUCTORS[name](anomaly_type , default_params=param_dict)


def parse_algorithm_argument(algonames):
    return [RPCA1, PCA_RPCA, RPCA3, PCA, RPCA4]


