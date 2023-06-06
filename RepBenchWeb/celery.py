from __future__ import absolute_import, unicode_literals
import os
import logging

import numpy as np
from ray.tune.search.hyperopt import HyperOptSearch
from ray.tune.search.nevergrad import NevergradSearch
from ray.tune.search.skopt import SkOptSearch

from recommendation.ray_tune.ray_tune_config import config as ray_tune_config

from celery import Celery, shared_task, signals
#
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RepBenchWeb.settings')

app = Celery('RepBenchWeb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.event_serializer = 'pickle'  # this event_serializer is optional. somehow i missed this when writing this solution and it still worked without.
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']


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
def flaml_search_task(self, settings, X_train, y_train, X_test, y_test, my_task_id):
    from RepBenchWeb.models import TaskData
    # automl = AutoML(**settings)
    normal_write = sys.stdout.write
    setting_metric = settings["metric"]
    print("MEEEETRIC", setting_metric)
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)

    for p_ in y_train:
        print(p_)
    def custom_metric(
            X_val, y_val, estimator, labels,
            X_train, y_train, weight_val=None, weight_train=None,
            *args,
    ):
        import time
        start = time.time()
        pred_time = (time.time() - start) / len(X_val)
        estimator.fit(X_train, y_train)
        # print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)
        y_pred = estimator.predict(X_val)
        score = metrics[setting_metric](y_pred, y_val)
        print(y_pred,score)

        estimator_name = str(estimator.__class__.__name__).split("Estimator")[0]
        if estimator_name == "LRL1Classifier":
            estimator_name = "LogisticRegression"
        # print(estimator)
        task_data.add_data({"score": score, "pred_time": pred_time,
                            "estimator": estimator_name, "config": {"model": estimator_name, **estimator.get_params()}})

        return score, {"pred_time": pred_time}

    # Initialize FLAML with custom metric
    automl = AutoML()

    settings["metric"] = custom_metric
    # print("start task")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        automl.fit(X_train=X_train, y_train=y_train, **settings, n_jobs=3, verbose=-3)

    automl._state.metric = setting_metric  # reset metric to original (we cant picke local objects)

    task_data.set_classifier(automl)
    task_data.set_done()

    # classifier = automl.model
    # try:
    #     print(classifier.feature_names_)
    # except:
    #     print(classifier.feature_names_in_)

    # print(X_train)
    # classifier.fit(X_train, y_train)
    # print(automl.best_estimator)
    # print("prediction")
    # for p in automl.predict(X_test):
    #     print(p)
    # print("DONE")
    # print(classifier.feature_importances_)

    # print("CLEERY DOOOOONE")
    # print(task_data)


# from recommendation.ray_tune.ray_tune_config import config as ray_tune_config


from ray.tune import Callback
from ray import tune, air
from ray.tune.search.zoopt import ZOOptSearch


@shared_task(bind=True)
def ray_tune_search_task(self, settings, X_train, y_train, X_test, y_text, my_task_id):
    from RepBenchWeb.models import TaskData
    task_data = TaskData.objects.get(task_id=my_task_id)
    task_data.set_celery_task_id(self.request.id)

    X = X_train
    y = y_train

    # check if X or y contains nan vlaues

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
        estimator = config.get("model")
        if estimator == "RandomForest":
            model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                           max_depth=config["max_depth"],
                                           min_samples_split=config["min_samples_split"])
        elif estimator == "ExtraTrees":
            model = ExtraTreesClassifier(n_estimators=config["n_estimators"],
                                         max_depth=config["max_depth"],
                                         min_samples_split=config["min_samples_split"],
                                         max_features=config["max_features"])

        elif estimator == "LogisticRegression":
            model = LogisticRegression(penalty="l1", C=config["C"], solver='liblinear')

        else:  # "LGBM"
            model = LGBMClassifier(n_estimators=config["n_estimators"],
                                   num_leaves=config["num_leaves"],
                                   learning_rate=config["learning_rate"],
                                   min_child_samples=config["min_child_samples"])
        model.fit(X, y)
        y_predict = model.predict(X_test)
        score = metrics[setting_metric](y_text, y_predict)
        return {"score": score}

    ray_tune_config = {
        "model": tune.choice(settings["estimator_list"]),
        "n_estimators": tune.randint(5, 30),
        "max_depth": tune.randint(3, 10),
        "min_samples_split": tune.randint(2, 6),
        "num_leaves": tune.randint(2, 30),
        "learning_rate": tune.choice(np.logspace(-4, 0, 500)),
        "min_child_samples": tune.randint(3, 15),
        "C": tune.choice(np.logspace(-5, 0, 500)),  # tune.loguniform(1e-3, 1)
        "max_features": tune.randint(3, 30),
        "max_leaf_nodes": tune.randint(3, 20),
    }

    search_alg = settings["optimizer"]

    if search_alg == "ZOOpt":
        zoopt_search_config = {
            "parallel_num": 3  # how many workers to parallel
        }

        zoopt_search = ZOOptSearch(
            algo="Asracos",  # only support Asracos currently
            budget=500000,  # must match `num_samples` in `tune.TuneConfig()`.
            # dim_dict=dim_dict,
            metric="score",
            mode="max",
            **zoopt_search_config
        )
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=50000, metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=500000, search_alg=zoopt_search))
    elif search_alg == "skopt":
        skopt_search = SkOptSearch(
            metric="score",
            mode="max",
        )

        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=skopt_search))

    elif search_alg == "nevergrad":
        import nevergrad as ng
        ng_search = NevergradSearch(
            optimizer=ng.optimizers.OnePlusOne,
            metric="score",
            mode="max",
        )

        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=ng_search))
    elif search_alg == "hyperopt":
        hyperopt_search = HyperOptSearch(
            metric="score", mode="max",
        )
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000, search_alg=hyperopt_search))

    elif search_alg == "default":
        tuner = tune.Tuner(train_model, param_space=ray_tune_config, run_config=air.RunConfig(callbacks=[MyCallback()]),
                           tune_config=tune.TuneConfig(time_budget_s=settings["time_budget"], metric="score", mode="max",
                                                       max_concurrent_trials=3,
                                                       num_samples=10000))

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
    task_data.set_classifier(model)

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
