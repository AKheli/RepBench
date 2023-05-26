from __future__ import absolute_import, unicode_literals
import os
import logging
import time
from recommendation.ray_tune.ray_tune_config import config as ray_tune_config
import numpy as np
import pandas as pd
from celery import Celery, shared_task, signals
# from contextlib import redirect_stdout
#
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from ray.tune.search.bayesopt import BayesOptSearch
from ray.tune.search.ax import AxSearch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepBenchWeb.settings')

app = Celery('RepBenchWeb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.event_serializer = 'pickle'  # this event_serializer is optional. somehow i missed this when writing this solution and it still worked without.
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']


# app.conf.task_serializer = 'pickle'

@signals.setup_logging.connect
def setup_celery_logging(**kwargs):  # disble logging for celery other wise ray tune does not function
    pass


from flaml import AutoML
import sys
import warnings

logger = logging.getLogger(__name__)


def revoke_task(task_id):
    from celery.contrib.abortable import AbortableAsyncResult
    task = AbortableAsyncResult(task_id)
    task.abort()
    print("CELERYYYY TAAAAASK STOPPPPPED")
    task.revoke(terminate=True)


from sklearn.metrics import f1_score, accuracy_score

metrics = {
    "accuracy": accuracy_score,
    "micro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='micro'),
    "macro_f1": lambda y_true, y_pred: f1_score(y_true, y_pred, average='macro')
}


@shared_task(bind=True)
def flaml_search_task(self, settings, X_train, y_train, my_task_id):
    print("start celery")
    from RepBenchWeb.models import TaskData
    # automl = AutoML(**settings)
    normal_write = sys.stdout.write
    setting_metric = settings["metric"]

    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)
    print("got task")

    def custom_metric(
            X_val, y_val, estimator, labels,
            X_train, y_train, weight_val=None, weight_train=None,
            *args,
    ):
        import time
        start = time.time()
        pred_time = (time.time() - start) / len(X_val)
        y_pred = estimator.predict(X_train)
        # print("score parameters" , y_train,y_pred)

        score = metrics[setting_metric](y_train, y_pred)
        estimator = str(estimator.__class__.__name__).split("Estimator")[0]
        print(estimator)
        task_data.add_data({"score": score, "pred_time": pred_time,
                            "estimator": estimator})
        return score, {"pred_time": pred_time}

    # Initialize FLAML with custom metric
    automl = AutoML()

    settings["metric"] = custom_metric
    print("start task")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        automl.fit(X_train=X_train, y_train=y_train, **settings, n_jobs=3, verbose=-3)

    automl._state.metric = setting_metric  # reset metric to original (we cant picke local objects)
    task_data.set_done()

    task_data.set_autoML(automl)
    print("CLEERY DOOOOONE")
    print(task_data)


# from recommendation.ray_tune.ray_tune_config import config as ray_tune_config


from ray import air, tune

from ray.tune import Callback


@shared_task(bind=True)
def ray_tune_search_task(self, settings, X_train, y_train, my_task_id):
    from ray import tune
    from RepBenchWeb.models import TaskData
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)

    X = X_train
    y = y_train

    # check if X or y contai nan vlaues

    setting_metric = settings["metric"]

    class MyCallback(Callback):
        def on_trial_result(self, iteration, trials, trial, result, **info):
            data_ = {"score": result["score"],
                     "estimator": result["config"]["model"],
                     "pred_time": result["time_this_iter_s"],
                     "config": result["config"].copy()
                     }

            # print("DATA", data_)
            task_data.add_data(data_)

    def train_model(config):
        estimator = config.get("model", "LGBM")
        if estimator == "RandomForest":
            model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                           max_depth=config["max_depth"],
                                           min_samples_split=config["min_samples_split"])
        elif estimator == "ExtraTrees":
            model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
                                         max_depth=config["max_depth"],
                                         min_samples_split=config["min_samples_split"])
        elif estimator == "LogisticRegression":
            model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')

        else:  # "LGBM"
            model = LGBMClassifier(n_estimators=config["n_estimators"],
                                   num_leaves=config["num_leaves"],
                                   learning_rate=config["learning_rate"],
                                   min_child_samples=config["min_child_samples"])
        model.fit(X, y)
        y_predict = model.predict(X)
        score = metrics[setting_metric](y, y_predict)
        return {"score": score}

    #ray_tune_config.pop("model", "")
    # ax_search = AxSearch()
    tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                       tune_config=tune.TuneConfig(time_budget_s=5, metric="score", mode="max", max_concurrent_trials=3,
                                                   num_samples=-1))
    t = time.time()



    # bayesopt = BayesOptSearch(metric="score", mode="max")
    # tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
    #                    tune_config=tune.TuneConfig(time_budget_s=5, metric="score", mode="max", max_concurrent_trials=3,
    #                                                num_samples=-1, search_alg=bayesopt)
    #                    )

    result_grid = tuner.fit()
    best_result = result_grid.get_best_result()
    best_config = best_result.config

    estimator = best_config.get("model", "LGBM")
    if estimator == "RandomForest":
        model = RandomForestClassifier(n_estimators=best_config["n_estimators"],
                                       max_depth=best_config["max_depth"],
                                       min_samples_split=best_config["min_samples_split"])
    elif estimator == "ExtraTrees":
        model = ExtraTreesClassifier(n_estimators=best_config["n_estimators"],
                                     max_depth=best_config["max_depth"],
                                     min_samples_split=best_config["min_samples_split"])
    elif estimator == "LogisticRegression":
        model = LogisticRegression(penalty="l1", C=best_config["C"], solver='liblinear')

    else:  # "LGBM"
        model = LGBMClassifier(n_estimators=best_config["n_estimators"],
                               num_leaves=best_config["num_leaves"],
                               learning_rate=best_config["learning_rate"],
                               min_child_samples=best_config["min_child_samples"])

    model.fit(X, y)
    task_data.set_done()
    print("DONE")
    # task_data.set_done()
    task_data.set_autoML(model)

# print(results.get_best_result(metric="score", mode="min").config)

# from RepBenchWeb.models import TaskData
# # import faulthandler
# from ray import tune
#
# # faulthandler.disable()
# # ray.init(log_to_driver=False, ignore_reinit_error=True,include_dashboard=False)
# # faulthandler.enable()
#
#
# task_data = TaskData(task_id=my_task_id, data_type="ray_tune", celery_task_id=self.request.id)
# task_data.save()
#
# X = pd.DataFrame.from_dict(X_train_dict)
# y = np.array(y_train_list)
# automl = AutoML(**settings)
# normal_write = sys.stdout.write
# setting_metric = settings["metric"]
# print(X)
# print(y)
#
# def train_model(config):
#     estimator = config.get("estimator", "LGBM")
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
#     model.fit(X, y)
#     accuracy = accuracy_score(y, model.predict(X))
#     print(accuracy)
#
#     estimator_name = str(model.__class__.__name__).split("Estimator")[0]
#
#     # task_data.add_data({"score": accuracy, "pred_time": -1,
#     #                     "estimator": estimator_name})
#     score = metrics[setting_metric](X, y)
#     print("TRAAAAAAning")
#     tune.report(setting_metric=score)
#
#
#
# # with warnings.catch_warnings():
# #     warnings.simplefilter("ignore")
#
# tuner = tune.Tuner(
#     train_model,
#     run_config=air.RunConfig(
#         callbacks=[MyCallback()]
#     )
# )
# tuner.fit()
#
# analysis = tuner.run(train_model, config=ray_tune_config, time_budget_s=settings["time_budget"],
#                     num_samples=1000)
#
# print(analysis.best_config)
# print(analysis.best_result)
# print(analysis.best_trial)
# task_data.set_autoML(automl)
# print("CLEERY DOOOOONE")
# print(task_data)

#
# def ray_tune_search_task_non_celery(settings, X_train_dict, y_train_list, my_task_id):
#     from RepBenchWeb.models import TaskData
#     # import faulthandler
#     from ray import tune
#
#     # faulthandler.disable()
#     # ray.init(log_to_driver=False, ignore_reinit_error=True,include_dashboard=False)
#     # faulthandler.enable()
#
#
#     task_data = TaskData(task_id=my_task_id, data_type="ray_tune", celery_task_id=-1)
#     task_data.save()
#
#     X = pd.DataFrame.from_dict(X_train_dict)
#     time.sleep(4)
#     y = np.array(y_train_list)
#     automl = AutoML(**settings)
#     normal_write = sys.stdout.write
#     setting_metric = settings["metric"]
#     print(X)
#     print(y)
#
#     def train_model(config):
#         estimator = config.get("estimator", "LGBM")
#         if estimator == "RandomForest":
#             model = RandomForestClassifier(n_estimators=config["n_estimators"],
#                                            max_depth=config["max_depth"],
#                                            min_samples_split=config["min_samples_split"])
#         elif estimator == "ExtraTrees":
#             model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
#                                          max_depth=config["max_depth"],
#                                          min_samples_split=config["min_samples_split"])
#         elif estimator == "LogisticRegression":
#             model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')
#
#         else:  # "LGBM"
#             model = LGBMClassifier(n_estimators=config["n_estimators"],
#                                    num_leaves=config["num_leaves"],
#                                    learning_rate=config["learning_rate"],
#                                    min_child_samples=config["min_child_samples"])
#
#         model.fit(X, y)
#         #
#         # accuracy = accuracy_score(y, model.predict(X))
#         #
#         # estimator_name = str(model.__class__.__name__).split("Estimator")[0]
#
#         # task_data_ = TaskData(task_id=my_task_id, data_type="ray_tune", celery_task_id=-1)
#         # task_data_.add_data({"score": accuracy, "pred_time": -1,
#         #                     "estimator": estimator_name})
#
#         print(X, y)
#         print(model.predict(X))
#         # score = metrics[setting_metric](X, y)
#         print("TRAAAAAAning")
#         tune.report(accuracy = 1)
#
#
#
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         analysis = tune.run(train_model, config=ray_tune_config, time_budget_s=settings["time_budget"],
#                             num_samples=1000)
#
#     print(analysis.best_config)
#     print(analysis.best_result)
#     print(analysis.best_trial)
#
