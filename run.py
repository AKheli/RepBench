import time

from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.senario_methods import repair_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *

scenarios = []
if __name__ == '__main__':
    input ="-scen vary_anomaly_size  -col 1  -data YAHOO.csv -anom a -algo IMR" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    args = init_parser(input)

    #data_files = read_data_files(args)
    file_name = args.data[0]


    cols = read_columns(args)
    scenario_constructor = read_scenario_argument(args)
    anomaly_type = read_anomaly_arguments(args)

    repair_algo_list = read_repair_algos(args)

    print("scenario:", scenario_constructor)
    print("repair algos:", repair_algo_list)



    injected_scenario = scenario_constructor(file_name, cols_to_inject = cols   ,anomaly_dict={"anomaly_type": anomaly_type})
    scenarios.append(injected_scenario)
    repair_scenario(injected_scenario, repair_algo_list)
    save_scenario(injected_scenario)
