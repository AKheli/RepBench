from Repair.algorithms_config import *
from Repair.IMR.imr_repair import IMR_repair
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import RPCA_repair
from Scenarios.Anomaly_Types import parse_anomaly_name
from Scenarios.scenario_types.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.ScenarioConfig import parse_scenario_name
from data_methods.Helper_methods import get_df_from_file


# def read_data_arguments(args):
#     data_arg = args.data[0]
#     print("data input" ,data_arg)
#     file_paths = parse_data_argument(args.data[0])
#     cols = [int(c) for c in args.col[0].split(",")]
#     results = {}
#     results["columns"] = cols
#     for file in file_paths:
#         data, name = get_df_from_file(file)
#         results[name] = data
#     return results

def read_columns(args):
    return  [int(c) for c in args.col[0].split(",")]

def read_data_files(args , check= True):
    print("data arg" , args.data[0])
    file_paths = parse_data_argument(args.data[0])
    if check:
        for file in file_paths:
            data,_ = get_df_from_file(file)
            print(data.head())
    return file_paths


def read_scenario_argument(args):
    scen = get_scenario(args.scenario[0])
    return scen

def read_anomaly_arguments(args):
    try:
        anomaly = parse_anomaly_name(args.anomaly_type[0])
    except Exception as e:
        print(args)
        raise e
    return anomaly


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





def parse_algorithm_argument(arg):
    for i in arg.split(","):
        i = i.upper()
    return [{"algorithm" : v , "params" : {} }for v in [RPCA_repair, SCREEN_repair, IMR_repair]]


def get_scenario(scenario_name):
    name = parse_scenario_name(scenario_name).lower()
    return SCENARIO_CONSTRUCTORS[name]


def read_repair_algos(args):
    # if hasattr(args, 'algox'):
    #     return parse_toml_file(args.algox)
    #elif hasattr(args, 'algo'):
    return parse_algorithm_argument(args.algo[0])




#
# def parse_toml_file(filename):
#     toml_output = load_toml_file()
#     results = []
#     for key in toml_output.keys():
#         algorithm = algo_mapper[key]
#         for params in toml_output[key].values():
#             results.append({"algorithm": algorithm,  "params": params,})
#             for param_name in params.keys():
#                 assert param_name in algorithm.__code__.co_varnames , f"toml file parse error" \
#                                                                       f"{param_name} not" \
#                                                                       f"found in " \
#                                                                       f"{algorithm.__code__.co_varnames[:algorithm.__code__.co_argcount]}"
#
#
#     return results




    # algos =  [ {"alg" : RPCA_repair , "n_columns": 2, "threshold": 2},
    #          RPCA_repair , "n_columns": 1, "threshold": 1},
    #          RPCA_repair: {"n_columns": 5, "threshold": 1}}
    #
    # return [ lambda additonal_params: k(**v.update(additonal_params)) for k,v in algos.items() ]
