import json
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..','..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.feature_extraction.load_features import load_data



filename = "recommendation/test/scores.txt"
load_string = "injection_parameters"


with open(filename, "r") as f:
    lines = f.readlines()

score_results = [json.loads(line) for line in lines]

for result in score_results:
    injection_parameters = result["injection_parameters"]
    injected_df , truth_df = load_data(injection_parameters, return_truth=True)
    injected_df_col = injected_df.iloc[:, injection_parameters["cols"]]
    truth_df_col = truth_df.iloc[:, injection_parameters["cols"]]
    print(injected_df_col)
    plt.plot(injected_df_col,label="injected")
    plt.plot(truth_df_col,label="truth")
    plt.legend()
    plt.show()

