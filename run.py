import time

from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.senario_methods import repair_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *


possible_scenarios = ["anomaly_size","ts_length","ts_nbr","base"]

scenarios = []

def split_comma_string(str, return_type  = str):
    return [  return_type(r) for r in  str.split(",") ]


if __name__ == '__main__':
    input ="-scenario ts_length  -col 1,2,3  -data YAHOO.csv -anom a -algo IMR" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    args = init_parser(input , scenario_choises = possible_scenarios)
    print(args)
    scen_param = args.scenario
    data_param = args.data

    cols = split_comma_string(args.col,int)

    scenario_constructor = SCENARIO_CONSTRUCTORS[scen_param]
    anomaly_type = parse_anomaly_name(args.a_type)
    repair_algo_list = read_repair_algos(args)




    injected_scenario = scenario_constructor(data_param, cols_to_inject = cols   ,anomaly_dict={"anomaly_type": anomaly_type})

    part_scenarios =  injected_scenario.scenarios

    for name ,values  in part_scenarios.items():
        data_params = {}
        data_params["truth"] = values["original"]
        data_params["injected"] = values["injected"]
        data_params["cols"] = values["columns"]
        for algo_info in repair_algo_list:
            algo_parameters = algo_info["params"]
            algo_parameters.update(data_params)

            result = algo_info["algorithm"](**algo_parameters)
            injected_scenario.add_repair(name,result ,result["name"])
        # with Pool() as pool:
        #     results = list(map(f, repair_algos))
        #     for repair in results:
        #         repairs[repair["name"]] = repair
        #
        # part_scenarios[scenario_part_name]["repairs"] = repairs


    save_scenario(injected_scenario)
