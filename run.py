import itertools
import os.path

from matplotlib import pyplot as plt

from Repair.Dimensionality_Reduction.CDrec.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.CDrec.weighted_CD_Rec_estimator import weighted_CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *
import logging
from datetime import datetime

current_path = os.getcwd()
folder = "MA"
path = folder.join(current_path.split(folder)[:-1]) + folder
os.chdir(path)

now = datetime.now()
dt_string = now.strftime("%d_%H:%M:%S")
try:
    os.makedirs("logs")
except:
    pass
logging.basicConfig(filename=f'logs/run_{dt_string}.log', level=logging.INFO)

possible_scenarios = ["cts_nbr"]  # ["anomaly_size", "ts_length", "ts_nbr", "anomaly_rate", "cts_nbr"]

repair_estimators = [IMR_estimator,CD_Rec_estimator, weighted_CD_Rec_estimator, Robust_PCA_estimator, SCREEN_estimator]

scenarios = []


def split_comma_string(str, return_type=str):
    return [return_type(r) for r in str.split(",")]


if __name__ == '__main__':
    input = "-scenario all  -col 0 -data all -anom a -algo IMR"  # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
    # input =  "-scenario all  -col 1  -data all  -anom a -algo IMR"

    data_dir = os.listdir("Data")
    args = init_parser(input=None, scenario_choises=possible_scenarios + ["all"], data_choices=data_dir + ["all"])
    scen_param = args.scenario
    data_param = args.data

    cols = split_comma_string(args.col, int)

    scenario_constructors = [SCENARIO_CONSTRUCTORS[scen_param]] if scen_param != "all" \
        else [SCENARIO_CONSTRUCTORS[scen] for scen in possible_scenarios]

    data_files = [f'{data_param}'.csv] if data_param != "all" \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]

    anomaly_type = parse_anomaly_name(args.a_type)

    scenario_constructors_data_names = itertools.product(scenario_constructors, data_files)

    # logging.info(
    #     f'{input}->cols:{cols},anomaly_type:{anomaly_type},scen and data {list(itertools.product(scenario_constructors, data_files))}')
    print(list(itertools.product(scenario_constructors, data_files)))
    print(repair_estimators)

    estimators = [estimator(columns_to_repair=cols) for estimator in repair_estimators]

    for (scenario_constructor, data_name) in itertools.product(scenario_constructors, data_files):
        for estim in estimators:
            injected_scenario: BaseScenario = scenario_constructor(data_name, cols_to_inject=cols,
                                                                   anomaly_type=anomaly_type)
            repair_algo_list = repair_estimators

            for name, train, test in injected_scenario.name_train_test_iter:
                data_params = {}
                data_params["truth"] = test["original"]
                injected = test["injected"]
                truth = test["truth"]

                data_params["cols"] = test["columns"]
                train_injected, train_truth = train["injected"], train["original"]

                estim.train(train_injected, train_truth)
                repair_out_put = estim.repair(injected , truth)
                injected_scenario.add_repair(name, repair_out_put, repair_out_put["name"])

                # logging.info(
                #     f'failed repair: scen: {scenario_constructor} . data_name: {data_name} , estimator: {estim}')
                # logging.error(f'{e})')

        save_scenario(injected_scenario)
        # logging.info(
        #     f'failed save: scen: {scenario_constructor} . data_name: {data_name} , estimator: {estim}')
        # logging.error(f'{e})')

print(12)
