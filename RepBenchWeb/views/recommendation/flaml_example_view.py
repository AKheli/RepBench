# from django.core.cache import cache
from sklearn.metrics import f1_score, accuracy_score

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
from recommendation.ray_tune.ray_tune_config import config as ray_tune_config

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

from recommendation.utils import *

multiclass_metrics = ['accuracy', 'macro_f1', 'micro_f1']

feature_file_name = "recommendation/results/features/validation_features"

algorithms_scores = parse_recommendation_results(feature_file_name)
best_algorithms = algorithms_scores['best_algorithm']
best_algorithms = best_algorithms.values.flatten()
feature_values = algorithms_scores['features']


train_split_r = 0.9
n_train_split = int(len(feature_values) * train_split_r)
train_split = np.random.choice(len(feature_values), n_train_split, replace=False)

X = feature_values.iloc[train_split, :]
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
    X = X.dropna(axis=1)


y : np.ndarray = best_algorithms[train_split]
from recommendation.encoder import encode
y = encode(y)

# get all other indices
def start_flaml(request):
    # time.sleep(10)
    test_split = np.setdiff1d(np.arange(len(feature_values)), train_split)
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
    from RepBenchWeb.models import TaskData

    try:
        TaskData.objects.get(task_id=task_id).delete()
    except TaskData.DoesNotExist:
        pass

    if tuner == "ray":
        task_data = TaskData(task_id=task_id, data_type="ray")
        task_data.save()
        ray_tune_search_task.delay(automl_settings, X, y, my_task_id=task_id)
    else:
        task_data = TaskData(task_id=task_id, data_type="flaml")
        task_data.save()
        flaml_search_task.delay(automl_settings, X, y, my_task_id=task_id)

    # from sklearn.ensemble import RandomForestClassifier
    # from lightgbm import LGBMClassifier
    # from sklearn.ensemble import ExtraTreesClassifier
    # from sklearn.linear_model import LogisticRegression
    # from ray.tune.search.bayesopt import BayesOptSearch
    #
    # from ray import tune
    # from RepBenchWeb.models import TaskData
    # # check if X or y contai nan vlaues
    #
    # setting_metric = automl_settings["metric"]
    #
    # metrics = {
    #     "accuracy": accuracy_score,
    #     "micro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='micro'),
    #     "macro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro')
    # }
    #
    # from ray.tune import Callback
    # class MyCallback(Callback):
    #     def on_trial_result(self, iteration, trials, trial, result, **info):
    #         data_ = {"score": result["score"],
    #                  # "estimator": result["config"]["model"],
    #                  "pred_time": result["time_this_iter_s"],
    #                  "config": result["config"].copy()
    #                  }
    #
    #         # print("DATA", data_)
    #
    # def train_model(config):
    #     estimator = config.get("model", "LGBM")
    #     if estimator == "RandomForest":
    #         model = RandomForestClassifier(n_estimators=config["n_estimators"],
    #                                        max_depth=config["max_depth"],
    #                                        min_samples_split=config["min_samples_split"])
    #     elif estimator == "ExtraTrees":
    #         model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
    #                                      max_depth=config["max_depth"],
    #                                      min_samples_split=config["min_samples_split"])
    #     elif estimator == "LogisticRegression":
    #         model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')
    #
    #     else:  # "LGBM"
    #         model = LGBMClassifier(n_estimators=config["n_estimators"],
    #                                num_leaves=config["num_leaves"],
    #                                learning_rate=config["learning_rate"],
    #                                min_child_samples=config["min_child_samples"])
    #
    #     t = time.time()
    #
    #     model.fit(X, y)
    #     y_predict = model.predict(X)
    #
    #     from sklearn.metrics import accuracy_score
    #     accuracy = accuracy_score(y, y_predict)
    #
    #     score = metrics[setting_metric](y, y_predict)
    #     return {"score": score}
    #
    # from ray.tune.search.ax import AxSearch
    # from ray import air, tune
    # ray_tune_config.pop("model","")
    # ax_search = AxSearch()
    # tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
    #                    tune_config=tune.TuneConfig(time_budget_s=5, metric="score", mode="max", max_concurrent_trials=3,
    #                                                num_samples=-1, search_alg=ax_search)
    #                    )
    # tuner.fit()
    print("sarch task initialized")
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
