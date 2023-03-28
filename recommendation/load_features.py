import json

import numpy as np
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from injection import inject_data_df
from recommendation.feature_extraction import extract_features

data_folder = "data/train"


def load_data(injection_parameters):
    """
    param: injection_parameters: dict
       injection_parameters = {
            "seed": seed,
            "factor": factor,
            "cols": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }
    """
    dataset = injection_parameters.pop("dataset")
    cols = injection_parameters["cols"]
    truth_df: pd.DataFrame = pd.read_csv(f"{data_folder}/{dataset}")
    n, m = truth_df.shape
    injected_df, col_range_map = inject_data_df(truth_df, **injection_parameters)
    assert injected_df.shape == truth_df.shape
    assert not np.allclose(injected_df.iloc[:, cols[0]].values, truth_df.iloc[:, cols[0]].values)
    return injected_df


def load_features(injection_parameters):
    """
    param: injection_parameters: dict
       injection_parameters = {
            "seed": seed,
            "factor": factor,
            "cols": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }

    return: features: dict of features for the selected column
    """
    injected_df = load_data(injection_parameters)
    print(injection_parameters["cols"][0], "AAAAAAAAAAAAAA")
    features = extract_features(injected_df, column=injection_parameters["cols"][0])
    return features


def get_injection_parameter_hashes_checker(file_name):
    if not os.path.exists(file_name):
        return lambda x: False

    with open(file_name, "r") as f:
        lines = f.readlines()

    injection_parameters_hashes = set()
    for line in lines:
        results_line = json.loads(line)
        injection_parameters = json.loads(line)["injection_parameters"]
        hash_value = hash(str(injection_parameters.items()))
        injection_parameters_hashes.add(hash_value)

    def checker(injection_parameters):
        hash_value = hash(str(injection_parameters.items()))
        return hash_value in injection_parameters_hashes

    return checker

def convert_features(file_name):
    """
    param: file_name: str , each line containing a dict with value "injection_parameters"
    returns: list of dicts where a featrues dict to each dict
    """
    with open(file_name, "r") as f:
        lines = f.readlines()
    results = []
    for line in lines:
        results_line = json.loads(line)
        injection_parameters = results_line["injection_parameters"]
        features = load_features(injection_parameters)
        results_line["features"] = features
        results.append(results_line)
    # store result to file
    with open(f"{file_name}_features", "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    return result


convert_features("recommendation/Scores/results")
