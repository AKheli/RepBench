from Repair.repair_algos.IMR.imr_repair import IMR_repair
from Repair.repair_algos.Robust_PCA.my_try import my_RPCA
from Scenarios.Anomaly_Types import parse_anomaly_name
from Scenarios.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.Scenario_Types import parse_scenario_name
from data_methods.Helper_methods import searchfiles, display_data_folder, get_df_from_file
from Repair.repair_algos.Robust_PCA.PCA_algorithms import *

def read_data_arguments(args):
    file_paths = parse_data_argument(args.data[0])
    cols = [ int(c) for c in args.col[0].split(",")]
    results = {}
    results["columns"] = cols
    for file in file_paths:
        data, name = get_df_from_file(file)
        results[name] = data
    return results


def read_injection_arguments(args):
    anomaly = parse_anomaly_argument(args.anomaly_type[0])
    scen = get_scenario(args.scenario[0], anomaly)
    return scen


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

def parse_algorithm_argument(arg):
    for i in arg.split[","]:
        i = i.upper()
    return [RPCA1, PCA_RPCA, RPCA3, PCA, RPCA4]


def get_scenario(scenario_name,anomaly_type , param_dict = None):
    name =  parse_scenario_name(scenario_name).lower()
    if param_dict is None:
        return SCENARIO_CONSTRUCTORS[name](anomaly_type)
    else:
        return  SCENARIO_CONSTRUCTORS[name](anomaly_type , default_params=param_dict)


def read_repair_algos(args):
    return parse_algorithm_argument(args.algo[0])

def parse_algorithm_argument(algonames):
    return [RPCA1 ,RPCA2, RPCA_no_train ,RPCA_no_train_2,IMR_repair] #, PCA_RPCA, RPCA3, PCA, RPCA4]




