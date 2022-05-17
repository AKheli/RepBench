import itertools
import os.path

import Scenarios.AnomalyConfig as at
import Repair.algorithms_config as algc
from Repair.repair_algorithm import RepairAlgorithm
from Scenarios.Scenario import Scenario
from Scenarios.scenario_saver.Scenario_saver import save_scenario
import Scenarios.ScenarioConfig as sc
from run_ressources.parser_init import init_parser
from run_ressources.parse_toml import load_toml_file




repair_estimators = algc.ALGORITHM_TYPES
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
    if args.alg is not None:
        estim_params = args.alg
        param_dicts = load_toml_file()
        repair_algos =  [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols , **param_dicts[rep_alg]) for rep_alg in estim_params] if "all" not in estim_params\
            else [RepairAlgorithm(estimator_name = rep_alg,columns_to_repair=cols, **param_dicts[rep_alg]) for rep_alg in repair_estimators]

    if args.algx is not None:
        filename = args.algx
        param_dict = load_toml_file(filename)
        repair_algos = []
        for alg_typ , params in param_dict.items():
            solo_params = { k:v  for k, v in params.items() if not isinstance(v,dict)}
            if len(solo_params) >0:
                alg = RepairAlgorithm(estimator_name=alg_typ, columns_to_repair=cols, **solo_params)
                repair_algos.append(alg)
            for name,inner_params in params.items():
                if isinstance(inner_params, dict):
                    inner_params["name"] = name
                    alg = RepairAlgorithm(estimator_name=alg_typ, columns_to_repair=cols, **inner_params)
                    repair_algos.append(alg)

    # map anomalies
    anomalies = [at.parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies

    for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomalies):
        scenario: Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)

        for estim in repair_algos:
             for name, train, test in scenario.name_train_test_iter:

                train_score = estim.train(**train.repair_inputs)
                repair_out_put = estim.repair(**test.repair_inputs)
                assert repair_out_put["type"] is not None
                test.add_repair(repair_out_put, repair_out_put["type"])

    #
        save_scenario(scenario,repair_plot=True)
    #

if __name__ == '__main__':
    main()

