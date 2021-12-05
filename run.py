import argparse

from Injection.inject import init_injection_parser, read_data_arguments, read_injection_arguments, inject, \
    add_injection_arguments_to_parser
from data_methods.Scenario_saver import save_injection_scenario
from run_ressources.input_parsers import parse_algorithm_argument


def init_parser():
    parser = argparse.ArgumentParser()
    add_injection_arguments_to_parser(parser)
    parser.add_argument("-algo", nargs=1, type=str, required=True)
    return  parser.parse_args()

def read_repair_algos(args):
    return parse_algorithm_argument(args.algo[0])



if __name__ == '__main__':
    args = init_parser()

    data_dict = read_data_arguments(args)
    scenario =  read_injection_arguments(args)
    anomaly_type = scenario.anomaly_type
    cols = data_dict.pop("columns")
    repair_algos = read_repair_algos(args)

    injected_results = inject(scenario,data_dict=data_dict,columns_to_inject= cols)
    save_injection_scenario(scenario, injected_results, data_dict)
    repair(injected_results)