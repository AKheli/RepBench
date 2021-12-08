import argparse
import json
from sys import getsizeof

from Injection.inject import get_scenario_data
from data_methods.Scenario_saver import  save_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import  read_repair_algos, read_data_arguments, \
    read_injection_arguments

if __name__ == '__main__':
    args = init_parser()

    data_dict = read_data_arguments(args)
    repair_algos = read_repair_algos(args)

    scenario = read_injection_arguments(args)
    print(scenario.scenario_type)
    print(scenario.anomaly_type)
    anomaly_type = scenario.anomaly_type
    cols = data_dict.pop("columns")

    for data_name , data in data_dict.items(): # go through the datasets
        injected_scenario = get_scenario_data(scenario, data=data, columns_to_inject=cols, train_split=0.3)

        to_repair_dicts = injected_scenario["scenario_data"]
        assert "train_class" in injected_scenario.keys()
        assert "train" in injected_scenario.keys()
        assert "train_original" in injected_scenario.keys()

        required_algorithm_params = ["train" , "train_class"]
        params = { p : injected_scenario[p] for p in required_algorithm_params}

        repairs = {}
        for part_scenario_name,part_scenario_data in to_repair_dicts.items():
            params["truth"] = part_scenario_data["original"]
            params["injected"] = part_scenario_data["injected"]

            repairs[part_scenario_name] = {}
            for algo in repair_algos:
                alg_results = algo(**params)
                repairs[part_scenario_name][algo.__name__] = alg_results

        save_scenario(data_name, scenario , injected_scenario ,repairs , cols = cols)
