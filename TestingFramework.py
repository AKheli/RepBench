import itertools
import os.path

import Scenarios.AnomalyConfig as at
from Repair.repair_algorithm import RepairAlgorithm
from Scenarios.Scenario import Scenario
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
import Scenarios.ScenarioConfig as sc
from Scenarios.scenario_types.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from run_ressources.parser_init import init_parser
from run_ressources.parse_toml import load_toml_file

current_path = os.getcwd()
folder = "MA"
path = folder.join(current_path.split(folder)[:-1]) + folder
os.chdir(path)


repair_estimators = ["rpca","screen","cdrec","imr"]
estimator_choices = repair_estimators + ["all"]

scenarios = [sc.ANOMALY_SIZE, sc.CTS_NBR , sc.ANOMALY_RATE  , sc.TS_LENGTH,sc.TS_NBR]
scenario_choices = scenarios + ["all"]

all_anomalies = [at.AMPLITUDE_SHIFT,at.DISTORTION,at.POINT_OUTLIER]
anomaly_choices =all_anomalies+["all"]

def main(input = None):
    """ input : args parameter when not run in console"""
    data_dir =  os.listdir("Data")
    data_dir_trim = [txt.split(".")[0] for txt in data_dir]
    args = init_parser( input = input,
                        estimator_choices = estimator_choices,
                        scenario_choices=scenario_choices ,
                        data_choices=data_dir_trim + ["all"],
                        anomaly_choices = anomaly_choices)

    scen_params = args.scenario
    data_params = args.data
    estim_params = args.alg
    anomaly_types_param = args.a_type

    # map scenario input
    cols = [0] #(args.col)
    scen_names = scenarios if "all" in scen_params else scen_params


    # map data input
    data_files = [f'{data_param}.csv' for data_param in data_params] if "all" not in data_params \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]

    # for name in scen_names:
    #     Scenario(name,data_files[0], cols_to_inject=cols,
    #              a_type=at.AMPLITUDE_SHIFT)

    # map repair estimator input
    param_dicts = load_toml_file()
    repair_algos =  [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols , **param_dicts[rep_alg]) for rep_alg in estim_params] if "all" not in estim_params\
        else [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols, **param_dicts[rep_alg]) for rep_alg in repair_estimators]

    # map anomalies
    anomalies = [at.parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies


    for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomalies):
        scenario: Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)

        for estim in repair_algos:
             for name, train, test in scenario.name_train_test_iter:

                 #estim.train(**train.get_repair_inputs)

                repair_out_put = estim.repair(**test.repair_inputs)
    #             #train_repair_output = estim.repair(train_injected, train_truth)
    #
    #             test.add_repair(name, train_repair_output, f'{repair_out_put["type"]}_train')
                test.add_repair(repair_out_put, repair_out_put["type"])

    #
        save_scenario(scenario,repair_plot=False)
    #

if __name__ == '__main__':
    main()

