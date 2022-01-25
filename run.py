import time

from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.senario_methods import repair_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *

scenarios = []
if __name__ == '__main__':
    input ="-scen vary_ts_length  -col 1  -data YAHOO.csv -anom a -algo IMR" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    args = init_parser()

    data_files = read_data_files(args)
    cols = read_columns(args)
    scenario_constructor = read_scenario_argument(args)
    anomaly_type = read_anomaly_arguments(args)

    repair_algo_list = read_repair_algos(args)

    print("scenario:", scenario_constructor)
    print("repair algos:", repair_algo_list)

    t = time.time()
    while time.time() - 3 < t:
        pass

    for data_file in data_files:  # go through the datasets
        injected_scenario = scenario_constructor(data_file, anomaly_dict={"anomaly_type": anomaly_type}
                                                        , cols_to_injected=cols)
        scenarios.append(injected_scenario)
        repair_scenario(injected_scenario, repair_algo_list)
        save_scenario(injected_scenario)
