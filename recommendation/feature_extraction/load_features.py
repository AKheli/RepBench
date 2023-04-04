import json

import numpy as np
import pandas as pd
import os

from injection import inject_data_df
from recommendation.feature_extraction.feature_extraction import extract_features

default_data_folder = "recommendation/datasets/train"


def load_data(injection_parameters, return_truth=True, data_folder=default_data_folder, row_cap=20000, col_cap=20):
    """
    Args:
    injection_parameters: dict = {
            "seed": seed,
            "factor": factor,
            "cols" (int): columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }
        return_truth (bool): Whether to return the original dataset as well as the injected dataset
            (default is True).
        data_folder (str): The path to the folder where the CSV dataset file is located (default is
            default_data_folder).
        row_cap (int): The maximum number of rows to load from the dataset file (default is 20000).
        col_cap (int): The maximum number of columns to load from the dataset file (default is 20).

    Returns:
        If return_truth is True, returns a tuple containing two pandas DataFrames: the injected dataset
        and the original dataset (before injection). If return_truth is False, returns only the injected
        dataset as a pandas DataFrame.

    """
    injection_parameters = injection_parameters.copy()
    dataset = injection_parameters.pop("dataset")
    cols = injection_parameters["cols"]
    truth_df: pd.DataFrame = pd.read_csv(f"{data_folder}/{dataset}")
    n, m = truth_df.shape

    # z-score  normalization and cutting
    truth_df = truth_df.iloc[:min(n, row_cap), :min(m, col_cap)]
    truth_df = (truth_df - truth_df.mean()) / truth_df.std()

    injected_df, col_range_map = inject_data_df(truth_df, **injection_parameters)
    assert injected_df.shape == truth_df.shape
    assert not np.allclose(injected_df.iloc[:, cols[0]].values, truth_df.iloc[:, cols[0]].values)

    # import matplotlib.pyplot as plt
    # plt.plot(injected_df.iloc[:, cols].values , color="red")
    #
    # plt.plot(truth_df.iloc[:, cols].values)
    # plt.show()
    if return_truth:
        return injected_df, truth_df
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
    injected_df, _ = load_data(injection_parameters)
    features = extract_features(injected_df, column=injection_parameters["cols"][0])
    return features


def get_injection_parameter_hashes_checker(file_name):
    if not os.path.exists(file_name):
        return lambda x: False

    with open(file_name, "r") as f:
        lines = f.readlines()

    injection_parameters_strings = set()
    for line in lines:
        injection_parameters = json.loads(line)["injection_parameters"]
        str_value = str(injection_parameters.values())
        injection_parameters_strings.add(str_value)

    def checker(injection_parameters):
        new_value = str(injection_parameters.values())
        return new_value in injection_parameters_strings

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
        with open(f"{file_name}_features", "a") as f:
            # for result in results:
            f.write(json.dumps(results_line) + "\n")

    return results
