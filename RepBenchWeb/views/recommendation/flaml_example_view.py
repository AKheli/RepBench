# from django.core.cache import cache
from RepBenchWeb.models import TaskData
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
import sys
import os
from RepBenchWeb.celery import flaml_search_task
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

feature_file_name = "recommendation/results/features/results_features"

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

    test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
    X_train = feature_values.iloc[train_split, :]
    y_train : np.ndarray = categories_encoded[train_split]

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

    print("ESTIMATOR LIST" , request.POST.get("estimator_list") )
    estimator_list = request.POST.get("estimator_list")
    estimator_list = estimator_list if isinstance(estimator_list, list) else estimator_list.split(",")

    automl_settings["estimator_list"] = estimator_list
    X_train_dict = X_train.to_dict()
    y_train_dict = y_train.tolist()
    task_id = token
    flaml_search_task.delay(automl_settings, X_train_dict, y_train_dict, my_task_id=task_id)


    return RepBenchJsonRespone({"status": "ok", "automl_settings": automl_settings, "task_id": task_id})


def retrieve_flaml_results(request):
    token = request.POST.get("csrfmiddlewaretoken")

    task_id = request.POST.get("task_id")
    print("task_id retrive" , task_id)
    print(TaskData.objects.filter(task_id=task_id))
    try:
        print("celery taskdata" , TaskData.objects.filter(task_id=task_id).last().data)
    except:
        print("no task data found")
        return RepBenchJsonRespone({"data": [] , "status": "running"})

    task_object = TaskData.objects.filter(task_id=task_id).last()
    data = task_object.data
    status = task_object.status
    return RepBenchJsonRespone({"data": data, "status": status})



def get_flaml_recommendation(request,setname):
    task_id = request.POST.get("task_id")
    task_object = TaskData.objects.filter(task_id=task_id).last()
    recommendation = task_object.get_recommendation(setname)
    return RepBenchJsonRespone(recommendation)
