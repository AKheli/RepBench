import itertools
import os.path

import  Scenarios.Anomaly_Types as at
from Repair.repair_algorithm import RepairAlgorithm
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

scenarios = [sc.ANOMALY_SIZE, sc.CTS_NBR]
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
    scenario_constructors = [SCENARIO_CONSTRUCTORS[scen] for scen in scenarios] if "all" in scen_params \
        else [SCENARIO_CONSTRUCTORS[scen] for scen in scen_params]

    # map data input
    data_files = [f'{data_param}.csv' for data_param in data_params] if "all" not in data_params \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]



    ##
    # map repair estimator input
    param_dicts = load_toml_file()
    repair_algos =  [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols , **param_dicts[rep_alg]) for rep_alg in estim_params] if "all" not in estim_params\
        else [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols, **param_dicts[rep_alg]) for rep_alg in repair_estimators]

    # map anomalies
    anomalies = [parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies


    for (scenario_constructor, data_name , anomaly_type) in itertools.product(scenario_constructors, data_files , anomalies):
        print(str(scenario_constructor).split(".")[-1][:-2], data_name ,anomaly_type )
        # todo map scenarioinput and anomaly input -> scen anonaly a ,  scen anonaly a,b if scenario suppoerst mutiple anomalies
        injected_scenario: BaseScenario = scenario_constructor(data_name, cols_to_inject=cols,
                                                               anomaly_type=anomaly_type)
        for estim in repair_algos:
            for name, train, test in injected_scenario.name_train_test_iter:
                data_params = {}
                data_params["truth"] = test["original"]
                injected = test["injected"]


                truth = test["truth"]
                data_params["cols"] = test["columns"]
                train_injected, train_truth = train["injected"], train["original"]

                injected_columns = train["columns"]
                estim.columns_to_repair = injected_columns
                #estim.train(train_injected, train_truth)

                injected_columns = test["columns"]
                estim.columns_to_repair = injected_columns
                repair_out_put = estim.repair(injected, truth)
                #train_repair_output = estim.repair(train_injected, train_truth)

                #injected_scenario.add_repair(name, train_repair_output, f'{repair_out_put["type"]}_train')
                injected_scenario.add_repair(name, repair_out_put, repair_out_put["type"])

                # logging.info(
                #     f'failed repair: scen: {scenario_constructor} . data_name: {data_name} , estimator: {estim}')
                # logging.error(f'{e})')

        save_scenario(injected_scenario,repair_plot=True)


if __name__ == '__main__':
    main()

