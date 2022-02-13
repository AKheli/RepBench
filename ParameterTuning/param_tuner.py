from ParameterTuning.dummy_search import Dummy_Search
from ParameterTuning.gridsearch import Grid_Search
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV, GridSearchCV, StratifiedKFold, KFold, LeaveOneOut
from skopt import BayesSearchCV

from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE


# tune a datset
# scenario tuner give scenario as parameter
from Scenarios.scenario_types.BaseScenario import BaseScenario


class ParamTuner():
    def __init__(self, n_jobs=-1):
        self.parameter_tuners = []
        self.n_jobs = n_jobs
        self.results = {}


    def get_params(self,param = None):
        if param is None:
            return [ (i["name"], i["params"]) for i in self.parameter_tuners]
        return [ (i["name"], i["params"][param]) for i in self.parameter_tuners]


    def init_tuner(self, tuner_name, param_grid, clf, tuner_params=None, cv=None):
        tuner_name = tuner_name.lower()[:2]
        skf = KFold(n_splits=2 ,shuffle=True, random_state=1)
        if tuner_name in ["ba"]:
            return BayesianOptimization(clf, param_grid, n_jobs=self.n_jobs)
        if tuner_name in ["gr", "gs"]:
            return GridSearchCV(clf, param_grid, n_jobs=self.n_jobs ,cv=skf)
        if tuner_name in ["bc"]:
            return BayesSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                 random_state=0 , cv=skf)
        if tuner_name in ["ha", "hg"]:
            return HalvingGridSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0)

        if tuner_name in ["du"]:
            return Dummy_Search(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0)
        if tuner_name in ["gn"]:
            return Grid_Search(clf, param_grid, n_jobs=self.n_jobs,
                                random_state=0)
        assert False, "tuner could not be passed"


    def add(self, repair_estimator, param_grid, tuner,
            cv=None, name = None):  # tuner params
        tuner = self.init_tuner(tuner, param_grid, repair_estimator , cv =  cv)
        self.parameter_tuners.append({"tuner":  tuner, "name" : name  if name is not None else type(tuner).__name__})

    def optimize_scenario(self, scenario : BaseScenario):

        result_name = f'{scenario.scenario_type}_{scenario.data_name}'
        self.results[result_name] = {}
        scenario_results = self.results[result_name]


        scenario_data = scenario.scenarios
        train_X,train_y = scenario.train["injected"] , scenario.train["original"]

        for tuner_dict in self.parameter_tuners:
            fig, axs =  plt.subplots(len(scenario_data.items())+1, figsize=(20, 7*(len(scenario_data.items())+1)), constrained_layout=True)
            # train tuner
            tuner = tuner_dict["tuner"]
            tuner_name = tuner_dict["name"]

            scenario_results[tuner_name] = {}
            tuner_scenario_result = scenario_results[tuner_name]
            print( tuner_name , "#"*50)

            timer = Timer()
            timer.start()
            tuner.fit(train_X,train_y)
            time = timer.get_time()
            estimator = tuner.best_estimator_
            best_params =  tuner.best_params_
            tuner_scenario_result["estimator"] = estimator
            tuner_scenario_result["params"] = best_params


            overal_train_error= estimator.error(train_X,train_y,plt=axs[0],name="train")
            tuner_scenario_result["train_score"] = overal_train_error
            tuner_dict["train_time"] = time

            axs_counter = 0
            for scenario_part_name, scenario_part in scenario_data.items():  # scenarios
                axs_counter += 1
                assert "injected" in scenario_part, print(scenario_part)
                validation_X , validation_y = scenario_part["injected"], scenario_part["original"]

                overal_train_error = estimator.error(validation_X, validation_y, plt=axs[axs_counter], name=scenario_part_name)

                tuner_scenario_result[scenario_part_name] = overal_train_error["ratio"]
                # axs_counter += 1
                # estimator.fit(validation_X) #todo
                # overal_train_error = estimator.error(validation_X, validation_y, plt=axs[axs_counter],
                #                                      name=f"refitted_{scenario_part_name}")
                # tuner_results = ["refitted", overal_train_error]
                # self.results.append(tuner_results)
                # estimator.components_ = c.copy()

            fig.savefig(f"ParameterTuning/results/{tuner_name}.svg")
            plt.close()
            plt.cla()
            plt.clf()




    def plot(self,injected,original,repair, cols , title = ""):
        repair = pd.DataFrame(repair)
        ax = repair.plot(title=title)
        for i, line in enumerate(ax.lines):
            if i not in cols:
                line.set_alpha(.1)
            else:
                plt.plot(injected.index,original.iloc[:,i],color="black")
                plt.plot(injected.index,injected.iloc[:,i],color="red",ls="dashed")

        return ax


class GridSearch():
    def _iter_test_indices(self, X, y=None, groups=None):
        super()._iter_test_indices(X,y,groups)
        for i in range(2):
            yield np.arange(X.shape[0])