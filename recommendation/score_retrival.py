import itertools

import pandas as pd
import numpy as np
import json

import os
import sys

from matplotlib import pyplot as plt

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from algorithms.param_loader import get_algorithm_params
from RepBenchWeb.BenchmarkMaps.repairCreation import create_injected_container
from injection.injection_config import AMPLITUDE_SHIFT, DISTORTION, POINT_OUTLIER
from algorithms.algorithm_mapper import algo_mapper
from algorithms.estimator import Estimator
from injection import inject_data_df
from datetime import datetime

# Get current date and time
now = datetime.now().strftime("%m-%d %H:%M:%S")

outputfile_name = f"recommendation/Scores/{now}"
log_file = f"recommendation/Scores/{now}_logs"
data_folder = "data/test"
factors = [1, 5, 10]
a_percentages = [1, 2, 5, 10, 20]
ts_cols = [[0]]
scores = ["rmse", "mae"]
datasets = ["bafu5k.csv", "elec.csv", "humidity.csv", "msd1_5.csv"]
a_types = [AMPLITUDE_SHIFT, DISTORTION, POINT_OUTLIER]


def append_to_file(data, filename):
    with open(filename, 'a') as f:
        f.write(json.dumps(data) + '\n')


injected_dfs = []
for factor, a_percentage, columns, score, dataset, a_type in itertools.product(factors, a_percentages, ts_cols, scores,
                                                                               datasets, a_types):
    # factor = factors[0]
    # columns = ts_cols[0]
    # dataset = datasets[0]
    # a_type = a_types[0]
    # a_percentage = a_percentages[0]

    truth_df: pd.DataFrame = pd.read_csv(f"{data_folder}/{dataset}")
    n, m = truth_df.shape
    col_list = [[i] for i in range(m)]

    for columns in col_list:
        seed = 100
        np.random.seed(seed)

        injection_parameters = {
            "seed": seed,
            "factor": factor,
            "columns": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percentage": a_percentage
        }
        alg_name = ""
        try:
            injected_df, col_range_map = inject_data_df(truth_df, a_type=a_type, cols=columns, factor=factor,
                                                        a_percent=a_percentage)
            injected_data_container = create_injected_container(truth_df, injected_df)
            injected_dfs.append(injected_df)

            alg_results = {}
            alg_name: str = "no alg"
            for alg_name, alg_constructor in algo_mapper.items():
                alg_results[alg_name] = {}

                parameters = get_algorithm_params(alg_name)
                alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs)[score]
                alg_results[alg_name] = {score: alg_score, "parameters": parameters}
            results = {"alg_results": alg_results, "injection_parameters": injection_parameters}
            append_to_file(results, outputfile_name)

        except Exception as e:
            injection_parameters["alg"] = alg_name
            injection_parameters["exception"] = str(e)
            append_to_file(injection_parameters,log_file)
