import os
from run_ressources.parse_toml import load_toml_file
import Scenarios.ScenarioConfig as sc
from run_ressources.parser_init import init_parser
import Repair.algorithms_config as algc
import Scenarios.AnomalyConfig as at


repair_estimators = algc.ALGORITHM_TYPES
estimator_choices = repair_estimators + ["all"]

scenarios = [sc.ANOMALY_SIZE, sc.CTS_NBR , sc.ANOMALY_RATE,sc.TS_LENGTH,sc.TS_NBR]
scenario_choices = scenarios + ["all"]

all_anomalies = [at.AMPLITUDE_SHIFT,at.DISTORTION,at.POINT_OUTLIER]
anomaly_choices =all_anomalies+["all"]

error_scores = ["rmse_full","rmse_partial","mae","mutual_info"]


def init_checked_parser(input):
    data_dir = os.listdir("Data")
    data_dir_trim = [txt.split(".")[0] for txt in data_dir]
    args = init_parser(input=input,
                       estimator_choices=estimator_choices,
                       scenario_choices=scenario_choices,
                       data_choices=data_dir_trim + ["all"],
                       anomaly_choices=anomaly_choices)

    return args


def parse_scen_names(args):
    scen_params = args.scenario
    scen_names = scenarios if "all" in scen_params else scen_params
    return scen_names

def parse_repair_algorithms(args):
    if "all" in args.alg:
        return algc.ALGORITHM_TYPES
    return args.alg

def parse_repair_algorithms_x(args):
    if args.algx is not None:
        filename = args.algx
        param_dict = load_toml_file(filename)
        repair_algos = []

        for alg_type, params in param_dict.items():
            direct_params = {k: v for k, v in params.items() if not isinstance(v, dict)}
            if len(direct_params) > 0:
                repair_algos.append({"type": alg_type , "name" : alg_type  , "params" : direct_params})
            for name, inner_params in params.items():
                if isinstance(inner_params, dict):
                    repair_algos.append({"type" : alg_type , "name" : name , "params" : inner_params})

        return repair_algos

def parse_data_files(args):

    data_dir = os.listdir("Data")

    data_params = args.data
    data_files = [f'{data_param}.csv' for data_param in data_params] if "all" not in data_params \
        else [d for d in data_dir if os.path.isfile(f"Data/{d}")]
    return data_files


def parse_anomaly_types(args):
    anomaly_types_param = args.a_type
    anomalies = [at.parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies
    return anomalies


def parse_training_arguments(args):
    train_method = args.train
    train_error = args.train_error

    return train_method, train_error

