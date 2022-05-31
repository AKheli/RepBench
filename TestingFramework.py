import itertools
import os.path

import toml
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

error_scores = ["rmse_full","rmse_partial","mae","mutual_info"]

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
    train_method = args.train
    anomaly_types_param = args.a_type
    train_error = args.train_error


    # map scenario input
    cols = [0] #(args.col)
    scen_names = scenarios if "all" in scen_params else scen_params


    # map data input
    data_files = [f'{data_param}.csv' for data_param in data_params] if "all" not in data_params \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]

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
            direct_params = { k:v  for k, v in params.items() if not isinstance(v,dict)}
            if len(direct_params) >0:
                alg = RepairAlgorithm(estimator_name=alg_typ, columns_to_repair=cols, **direct_params)
                repair_algos.append(alg)
            for name,inner_params in params.items():
                if isinstance(inner_params, dict):
                    inner_params["name"] = name
                    alg = RepairAlgorithm(estimator_name=alg_typ, columns_to_repair=cols, **inner_params)
                    repair_algos.append(alg)

    # map anomalies
    anomalies = [at.parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies

    # initialize all scenarios first to check if the can be created
    # for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomalies):
    #     print(f'running repair on {data_name} with scen type {scen_name}')
    #     scenario: Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)
    #     del scenario

    for (scen_name, data_name , anomaly_type) in itertools.product(scen_names, data_files , anomalies):
        try:
            scenario: Scenario = Scenario(scen_name,data_name, cols_to_inject=cols,a_type=anomaly_type)
        except Exception as e:
            print(f'running repair on {data_name} with scen type {scen_name} failed')
            raise e
        print(f'running repair on {data_name} with scen type {scen_name}')

        for repair_alg in repair_algos:
             for name, train_part, test_part in scenario.name_train_test_iter:
                params = find_or_load_train(repair_alg,train_error,train_part,data_name,train_method = train_method)
                #params = estim.train(**train_part.repair_inputs, error_score=train_error, train_method=train_method)
                repair_alg.set_params(params)
                repair_out_put = repair_alg.repair(**test_part.repair_inputs)
                assert repair_out_put["type"] is not None
                test_part.add_repair(repair_out_put, repair_out_put["type"])

        save_scenario(scenario, repair_plot=True,  res_name=args.rn)
    #

from pathlib import Path
def find_or_load_train(estimator,error_score,train_part,data_name,train_method):
    alg_type = estimator.alg_type
    path = f"TrainResults/{alg_type}/{data_name}/"
    file_name = "train_results.toml"
    file_exists = True
    try:
        toml_dict = toml.load(f'{path}{file_name}')
    except:
        file_exists = False

    Path(path).mkdir(parents=True, exist_ok=True)

    part_repr = str(train_part)
    # try to get parameters from file
    try:
        params = toml_dict[part_repr][error_score][train_method]
        assert isinstance(params,dict)
        return params
    except:
        params = estimator.train(**train_part.repair_inputs, error_score=error_score , train_method = train_method)

        if not file_exists:
            toml_dict = {}
        if part_repr not in toml_dict:
            toml_dict[part_repr] = {error_score: {train_method : params}}
        elif error_score not in toml_dict[part_repr]:
            toml_dict[part_repr][error_score] = {train_method : params}
        elif train_method not in toml_dict[part_repr][error_score]:
            toml_dict[part_repr][error_score][train_method] = params

        with open(f'{path}{file_name}', 'w') as f:
            toml.dump(toml_dict,f,encoder=toml.TomlNumpyEncoder(preserve=True))

        return params

if __name__ == '__main__':
    main()

