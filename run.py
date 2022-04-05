import itertools
import os
import os.path
from matplotlib import pyplot as plt

from Repair.Dimensionality_Reduction.CDrec.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *

current_path = os.getcwd()
folder = "MA"
path =  folder.join(current_path.split(folder)[:-1])+folder
os.chdir(path)

possible_scenarios = ["anomaly_size","ts_length","ts_nbr","base"]




repair_estimators = [CD_Rec_estimator] # Robust_PCA_estimator,SCREEN_estimator ,

scenarios = []

def split_comma_string(str, return_type  = str):
    return [  return_type(r) for r in  str.split(",") ]


if __name__ == '__main__':
    #input ="-scenario all  -col 0,1,2  -data batch10.txt -anom p -algo IMR" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    input =  "-scenario all  -col 1  -data all  -anom p -algo IMR"
    print(os.listdir())

    data_dir = os.listdir("Data")
    args = init_parser(input=input, scenario_choises = possible_scenarios+["all"] , data_choices = data_dir+["all"])
    scen_param = args.scenario
    data_param = args.data
    print(data_param)

    cols = split_comma_string(args.col,int)

    scenario_constructors = [SCENARIO_CONSTRUCTORS[scen_param]] if scen_param != "all" \
        else [SCENARIO_CONSTRUCTORS[scen] for scen in possible_scenarios]

    data_files = [data_param] if data_param != "all" \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]


    anomaly_type = parse_anomaly_name(args.a_type)

    scenario_constructors_data_names = itertools.product(scenario_constructors,data_files)
    for (scenario_constructor , data_name ) in scenario_constructors_data_names:
        injected_scenario : BaseScenario = scenario_constructor(data_name, cols_to_inject = cols   ,anomaly_dict={"anomaly_type": anomaly_type})

        repair_algo_list = repair_estimators



        for esitmator in repair_estimators:
            estim = esitmator(columns_to_repair=cols)
            for name ,train , test in injected_scenario.name_train_test_iter:
                data_params = {}
                data_params["truth"] = test["original"]
                injected = test["injected"]
                data_params["cols"] = test["columns"]
                train_injected , train_truth = train["injected"] , train["original"]
                # train_truth.plot()
                # plt.show()
                # train_injected.plot()
                # plt.show()
                # train["class"].astype(int).plot()
                # plt.show()


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
