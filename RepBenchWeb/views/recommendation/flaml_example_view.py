from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import sys
import os

import numpy as np
from sklearn.preprocessing import LabelEncoder
import time

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.flaml_search import flaml_search, flaml_search_advanced_output, flaml_search_multiprocess
from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/results_features"

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

train_split_r = 0.5
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)

# get all other indices
test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
X_train = feature_values.iloc[train_split, :]
X_test = feature_values.iloc[test_split, :]
y_train, y_test = categories_encoded[train_split], categories_encoded[test_split]




flaml_processes_queues_and_times = {}


def start_flaml(request):
    time_budget = 40
    automl_settings = {
        "time_budget": time_budget,  # in seconds
        "metric": "accuracy",  # accuracy , micro_f1, macro_f1
        "task": 'classification',
        "log_file_name": "recommendation/logs/flaml.log",
        "estimator_list": ['lgbm', 'rf', 'xgboost' , 'extra_tree' , 'lrl1']
    }

    token = request.POST.get("csrfmiddlewaretoken")

    if token in flaml_processes_queues_and_times:
        del flaml_processes_queues_and_times[token]

    flaml_process, out_put_queue = flaml_search_multiprocess(automl_settings, X_train, y_train)

    start_time = time.time()
    flaml_processes_queues_and_times[token] = (flaml_process,out_put_queue,start_time)
    return RepBenchJsonRespone({"status": "ok" , "automl_settings": automl_settings})

import re
regex = r"at\s+(\d+\.\d+)s,\s*estimator\s+(\w+)'s\s+best\s+error=(\d+\.\d+),\s*best\s+estimator\s+(\w+)'s\s+best\s+error=(\d+\.\d+)"
from _queue import Empty


def retrieve_flaml_results(request):
    print("retrieve_flaml_results")
    status = "running"
    token = request.POST.get("csrfmiddlewaretoken")
    try:
        flaml_process, out_put_queue, start_time = flaml_processes_queues_and_times[token]
    except KeyError:
        return RepBenchJsonRespone({"results": [] , "status":"finished"})


    results = []
    while True:
        try:
            output = out_put_queue.get(timeout=10, block=False)
            if "at" in output:
                match = re.search(regex, output)
                if match:
                    result = {"time": float(match.group(1)),
                              "estimator": match.group(2),
                              "error": float(match.group(3)),
                              "best_estimator": match.group(4),
                              "best_error": float(match.group(5))
                              }
                    print(result)
                    results.append(result)
                    print(output.split("cut")[-1] if "cut" in output else "")

        except Empty:
                break
    if not flaml_process.is_alive():
        print("process is dead")
        flaml_processes_queues_and_times.pop(token,"")
        flaml_process.join()
        status = "finished"

    return RepBenchJsonRespone({"results": results , "status":status})
