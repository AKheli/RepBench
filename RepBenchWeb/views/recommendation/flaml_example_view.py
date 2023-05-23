# from django.core.cache import cache
from RepBenchWeb.models import TaskData
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import sys
import os
from RepBenchWeb.celery import flaml_search_task , ray_tune_search_task
import numpy as np
from sklearn.preprocessing import LabelEncoder
import time
from django.core.cache import cache

from RepBenchWeb.views.utils.cleanup_task import flaml_processes_queues_and_times, kill_process, \
    to_many_requests_response

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/validation_features"

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']

encoder = LabelEncoder()
categories_encoded = encoder.fit_transform(best_algorithms)

train_split_r = 0.9
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)

# get all other indices
def start_flaml(request):
    print("START" , dict(request.POST))
    # time.sleep(10)

    test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
    X_train = feature_values.iloc[train_split, :]
    y_train : np.ndarray = categories_encoded[train_split]
    print("X_train" , X_train.shape)
    time.sleep(4)
    automl_settings = {
        "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
        "task": 'classification',
        "log_file_name": "recommendation/logs/flaml.log",
        "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
    }

    token = request.POST.get("csrfmiddlewaretoken")
    automl_settings["time_budget"] = int(request.POST.get("time_budget",20))
    automl_settings["metric"] = request.POST.get("metric","accuracy")
    automl_settings["task"] = "classification"
    tuner = request.POST.get("tuner")


    print("ESTIMATOR LIST" , request.POST.get("estimator_list") )
    estimator_list = request.POST.get("estimator_list")
    estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")

    automl_settings["estimator_list"] = estimator_list

    task_id = request.POST.get("task_id")

    X = X_train
    y = y_train
    if X.isnull().values.any():
        nan_columns = X.columns[X.isnull().any()].tolist()
        if nan_columns:
            print("Columns containing NaN values:", nan_columns)

        nan_rows = X[X.isnull().any(axis=1)]
        if not nan_rows.empty:
            print("Row indices containing NaN values:\n", nan_rows.index)
        else:
            print("No rows contain NaN values.")
        print("X contains NaN values.")
        X_train = X.dropna(axis=1)

    else:
        print("X does not contain NaN values.")


    X_train_dict = X_train.to_dict()
    y_train_dict = y_train.tolist()
    # For numpy array
    if np.isnan(y).any():
        print("y contains NaN values.")
    else:
        print("y does not contain NaN values.")
    print("AFTER NAN CHECK")
    TaskData.objects.filter(task_id=task_id).delete()

    if tuner == "ray":
        ray_tune_search_task.delay(automl_settings, X_train_dict, y_train_dict, my_task_id=task_id)
    else:
        flaml_search_task.delay(automl_settings, X_train_dict, y_train_dict, my_task_id=task_id)

    return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})


def retrieve_flaml_results(request):
    token = request.POST.get("csrfmiddlewaretoken")

    task_id = request.POST.get("task_id")
    print("task_id retrive" , task_id)

    for i in range(25):
        if TaskData.objects.filter(task_id=task_id).exists():
            break
        else:
            time.sleep(0.3)

    print(TaskData.objects.filter(task_id=task_id))
        # print("failed to find task object")
        # time.sleep(2)

    task_data = TaskData.objects.filter(task_id=task_id).last()
    data = task_data.data
    status = task_data.status
    if task_data.is_running():
        return RepBenchJsonRespone({"data": data , "status": status})
    if task_data.is_done():
        # task_data.get_recommendation("test")
        return RepBenchJsonRespone({"data": data , "status": status})



def flaml_prediction(request,setname):
    task_id = request.POST.get("task_id")
    task_object = TaskData.objects.filter(task_id=task_id).last()
    print("TAAASK OBKECT , " , task_object , task_id)

    prediction = task_object.get_recommendation(setname)
    return RepBenchJsonRespone(prediction)
