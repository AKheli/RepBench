import itertools
import pandas as pd
import numpy as np
import json
import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.feature_extraction.load_features import get_injection_parameter_hashes_checker
from algorithms.param_loader import get_algorithm_params
from RepBenchWeb.BenchmarkMaps.repairCreation import create_injected_container
from injection.injection_config import AMPLITUDE_SHIFT, DISTORTION, POINT_OUTLIER
from algorithms.algorithm_mapper import algo_mapper
from injection import inject_data_df
from datetime import datetime

# Get current date and time
now = datetime.now().strftime("%m-%d %H:%M:%S")

outputfile_name = f"recommendation/results/{'results_ucr'}"
log_file = f"recommendation/logs/{now}_logs"
factors = [1, 5, 10]
a_percentages = [1, 2, 5, 10, 20]
ts_cols = [[0]]
scores = ["rmse", "mae"]
datasets =  os.listdir("recommendation/datasets/train")  #["smd1_5.csv"]
data_folder = "recommendation/datasets/train"

a_types = [AMPLITUDE_SHIFT, DISTORTION, POINT_OUTLIER]


def append_to_file(data, filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('')

    with open(filename, 'a') as f:
        if isinstance(data, dict):
            f.write(json.dumps(data) + '\n')
        else:
            f.write(data + '\n')


injected_dfs = []
already_computed_checker = get_injection_parameter_hashes_checker(outputfile_name)

for factor, a_percentage, columns, score, dataset, a_type in itertools.product(factors, a_percentages, ts_cols, scores,
                                                                               datasets, a_types):
    # factor = factors[0]
    # columns = ts_cols[0]
    # dataset = datasets[0]
    # a_type = a_types[0]
    # a_percentage = a_percentages[0]

    truth_df: pd.DataFrame = pd.read_csv(f"{data_folder}/{dataset}")
    #cap the number of rows columns at 30
    n, m = truth_df.shape
    col_list = [[i] for i in range(m)]

    for columns in col_list:
        seed = 100
        np.random.seed(seed)

        injection_parameters = {
            "seed": seed,
            "factor": factor,
            "cols": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }
        alg_name = ""
        try:
            if already_computed_checker(injection_parameters):
                print("Already computed")
                continue

            injected_df, col_range_map = inject_data_df(truth_df, a_type=a_type, cols=columns, factor=factor,
                                                        a_percent=a_percentage)

            print("file", dataset)
            print("injected_df", injected_df)

            assert len(injected_df) == len(truth_df)
            assert len(injected_df.columns) == len(truth_df.columns)
            assert not np.allclose(injected_df.values,truth_df.values) ,\
                [(truth_df.iloc[col,ranges], injected_df.iloc[col,ranges]-truth_df.iloc[col,ranges[0]]) for col,ranges in  col_range_map.items()]

            injected_data_container = create_injected_container(truth_df, injected_df)
            injected_dfs.append(injected_df)

            alg_results = {}
            alg_name: str = "no alg"
            for alg_name, alg_constructor in algo_mapper.items():
                print(alg_name)
                alg_results[alg_name] = {}

                parameters = get_algorithm_params(alg_name)
                alg_score = alg_constructor(**parameters).scores(**injected_data_container.repair_inputs)[score]
                alg_results[alg_name] = {score: alg_score, "parameters": parameters}
            results = {"alg_results": alg_results, "injection_parameters": injection_parameters}
            append_to_file(results, outputfile_name)

        except Exception as e:
            raise e
            import traceback

            print("Exception", e)
            print("failed to compute", alg_name,
                  "with", injection_parameters,
                  "with exception", e,
                  "of type", type(e).__name__, traceback.format_exc())
            injection_parameters["alg"] = alg_name
            injection_parameters["exception"] = traceback.format_exc()
            injection_parameters["exception_type"] = type(e).__name__
            append_to_file(injection_parameters, log_file)
