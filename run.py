import time

from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.senario_methods import repair_scenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *


possible_scenarios = ["anomaly_size","ts_length","ts_nbr","base"]




repair_estimators = [Robust_PCA_estimator,SCREEN_estimator] # , Robust_PCA_estimator]

scenarios = []

def split_comma_string(str, return_type  = str):
    return [  return_type(r) for r in  str.split(",") ]


if __name__ == '__main__':
    #input ="-scenario all  -col 0,1,2  -data batch10.txt -anom p -algo IMR" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    args = init_parser( scenario_choises = possible_scenarios+["all"])
    scen_param = args.scenario
    data_param = args.data

    cols = split_comma_string(args.col,int)

    if scen_param != "all":
        scenario_constructors = [SCENARIO_CONSTRUCTORS[scen_param]]
    else:
        scenario_constructors = [SCENARIO_CONSTRUCTORS[scen] for scen in possible_scenarios]

    anomaly_type = parse_anomaly_name(args.a_type)

    for scenario_constructor in scenario_constructors:
        injected_scenario = scenario_constructor(data_param, cols_to_inject = cols   ,anomaly_dict={"anomaly_type": anomaly_type})
        repair_algo_list = repair_estimators

    
        part_scenarios =  injected_scenario.scenarios

        for esitmator in repair_estimators:
            estim = esitmator(columns_to_repair=cols)
            for name ,values  in part_scenarios.items():
                data_params = {}
                data_params["truth"] = values["original"]
                injected = values["injected"]
                data_params["cols"] = values["columns"]
                print(values)
                train = values["train"]
                train_injected , train_truth = train["injected"] , train["original"]

                estim.train(train_injected,train_truth)
                repair_out_put = estim.repair(injected)
                injected_scenario.add_repair(name,repair_out_put ,repair_out_put["name"])
            # with Pool() as pool:
            #     results = list(map(f, repair_algos))
            #     for repair in results:
            #         repairs[repair["name"]] = repair
            #
            # part_scenarios[scenario_part_name]["repairs"] = repairs


        save_scenario(injected_scenario)
