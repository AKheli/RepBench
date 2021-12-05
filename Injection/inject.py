import argparse
import sys


sys.path.append('../') # always run from the toplevel folder
from Scenarios.TSLengthScenario import TSLengthScenario
from data_methods.Helper_methods import searchfile, get_df_from_file, display_data_folder
from data_methods.Scenario_saver import save_injection_scenario
from run_ressources.input_parsers import *


def add_injection_arguments_to_parser(parser):
    parser.add_argument("-data", "-d", nargs=1, type=str, default="None")
    parser.add_argument("-col", "-c", nargs=1, type=str, default=["0"])
    parser.add_argument('-save', nargs="*", type=str, default=False)
    parser.add_argument('-anomaly_type', '-at', nargs=1, default="amp")
    parser.add_argument("-scenario", nargs=1, type=str, required=True)
    return parser

def init_injection_parser():
    parser = argparse.ArgumentParser()
    parser = add_injection_arguments_to_parser(parser)
    return  parser.parse_args()

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


def inject(scen , data_dict , columns_to_inject):
    """Params
    scen  : Scenario
    anomaly : AnomalyType
    data_dict : { data_name1 : df1 , ...  "columns" = [ints..]}

    Returns:
    dictionary { data_name : [df1_to_repair , ....]
    """
    results = {}
    for name, data in data_dict.items():
        injected = scen.transform_df(data, cols=columns_to_inject)
        results[name] = injected
    return results


if __name__ == '__main__':
    args = init_injection_parser()
    data_dict = read_data_arguments(args)
    scenario =  read_injection_arguments(args)
    cols = data_dict.pop("columns")
    injected_results = inject(scenario,data_dict=data_dict,columns_to_inject= cols)
    save_injection_scenario(scenario, injected_results, data_dict)

