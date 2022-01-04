from Repair.Algorithms_File import *
from Repair.IMR.imr_repair import IMR_repair, IMR_repair_random
from Repair.Robust_PCA.PCA_algorithms import RPCA1, RPCA3
from Repair.Robust_PCA.RPCAestimation.RPCA_linmod import RPCA_lindmod
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import RPCA_repair
from Repair.Screen.SCREEN_repair import SCREEN_repair

from Scenarios.Anomaly_Types import parse_anomaly_name
from Scenarios.scenario_types.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.scenario_types.Scenario_Types import parse_scenario_name
from data_methods.Helper_methods import searchfiles, display_data_folder, get_df_from_file
from run_ressources.parse_toml import load_toml_file


def read_data_arguments(args):
    file_paths = parse_data_argument(args.data[0])
    cols = [int(c) for c in args.col[0].split(",")]
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
        print(filename_paths, "paths")
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


def get_scenario(scenario_name, anomaly_type, param_dict=None):
    name = parse_scenario_name(scenario_name).lower()
    if param_dict is None:
        return SCENARIO_CONSTRUCTORS[name](anomaly_type)
    else:
        return SCENARIO_CONSTRUCTORS[name](anomaly_type, default_params=param_dict)


def read_repair_algos(args):
    return parse_algorithm_argument(args.algo[0])


algo_mapper = {IMR: IMR_repair, RPCA: RPCA_repair, SCREEN: SCREEN_repair}


def parse_toml_file(filename):
    toml_output = load_toml_file()
    results = []
    for key in toml_output.keys():
        algorithm = algo_mapper[key]
        for params in toml_output[key].values():
            results.append({"algorithm": algorithm, "algo": algorithm, "params": params, "parameters": params})
            for param_name in params.keys():
                assert param_name in algorithm.__code__.co_varnames , f"toml file parse error" \
                                                                      f"{param_name} not" \
                                                                      f"found in " \
                                                                      f"{algorithm.__code__.co_varnames[:algorithm.__code__.co_argcount]}"


    return results


#def parse_default(repair_algorithms , filename = toml_default ):



def parse_algorithm_argument(algos) -> [dict]:
    algos = parse_anomaly_argument(algos)

    """
    returns list of dicts [{algo: ,params: } , ...]
    """
    return parse_toml_file(algos)

    # algos =  [ {"alg" : RPCA_repair , "n_columns": 2, "threshold": 2},
    #          RPCA_repair , "n_columns": 1, "threshold": 1},
    #          RPCA_repair: {"n_columns": 5, "threshold": 1}}
    #
    # return [ lambda additonal_params: k(**v.update(additonal_params)) for k,v in algos.items() ]
