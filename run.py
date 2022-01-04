from multiprocessing import Pool

from Injection.inject import get_scenario_data
from Scenarios.scenario_saver.Scenario_saver import  save_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import  read_repair_algos, read_data_arguments, \
    read_injection_arguments


def repair_scenario(injected_scenario ,repair_algos):
    part_scenarios = injected_scenario["scenario_data"]

    params = {}
    params["train"] = injected_scenario["train"]
    params["train_class"] = injected_scenario["train_class"]

    for scenario_part_name in part_scenarios.keys():
        part_scenario = part_scenarios[scenario_part_name]
        params["truth"] = part_scenario["original"]
        params["injected"] = part_scenario["injected"]
        params["cols"] = part_scenario["columns"]
        repairs = {}

        # for algo_info in repair_algos:
        #     algo_info["params"].update(params)
        #     print("AAAAAa",algo_info["params"])
        #
        #     alg_results = algo_info["algo"](**algo_info["params"])
        #     repairs[algo.__name__] = alg_results

        global f
        def f(algo_info ):

            pre_params = algo_info["params"]
            pre_params.update(params)
            result = algo_info["algo"](**pre_params)
            #print(f'done : {algo_info["algo"]}')
            return result

        with Pool() as pool:
            results = list(map( f, repair_algos))
            for repair in results:
                repairs[repair["name"]] = repair

        part_scenarios[scenario_part_name]["repairs"] = repairs
    return injected_scenario

if __name__ == '__main__':
    #"-scen vary  -col 0  -data YAHOO.csv -anom a -algo 1 "
    args = init_parser()


    data_dict = read_data_arguments(args)
    scenario = read_injection_arguments(args)

    anomaly_type = scenario.anomaly_type

    cols = data_dict.pop("columns")

    repair_algo_list= read_repair_algos(args)



    for data_name , data in data_dict.items(): # go through the datasets
        injected_scenario = get_scenario_data(scenario, data=data, columns_to_inject=cols, train_split=0.3)
        repaired_scenario = repair_scenario(injected_scenario ,repair_algo_list )
        repaired_scenario["data_name"] = data_name
        repaired_scenario["scenario_type"] = scenario
        save_scenario(repaired_scenario)
