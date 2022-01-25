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
class ParamTuner():
    def __init__(self, n_jobs=-1, classification=False):
        self.parameter_tuners = []
        self.n_jobs = n_jobs
        self.classification = classification

    def get_params(self,param = None):
        if param is None:
            return [ (i["name"], i["params"]) for i in self.parameter_tuners]
        return [ (i["name"], i["params"][param]) for i in self.parameter_tuners]


    def init_tuner(self, tuner_name, param_grid, clf, tuner_params=None, cv=None):
        assert tuner_name.lower()[:2] in ["ba", "gr", "gs", "ha", "hg", "bc"], "tuner could not be passed"
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

    def add(self, repair_estimator, param_grid, tuner,
            cv=None, name = None):  # tuner params
        tuner = self.init_tuner(tuner, param_grid, repair_estimator , cv =  cv)
        self.parameter_tuners.append({"tuner":  tuner, "name" : name  if name is not None else type(tuner).__name__})

    def optimize_scenario(self, scenario):
        scenario_data = scenario["scenario_data"]
        train_X,train_y = scenario["train"] , scenario["train_original"]

        for tuner_dict in self.parameter_tuners:
            fig, axs =  plt.subplots(len(scenario_data.items())+1, figsize=(20, 7*(len(scenario_data.items())+1)), constrained_layout=True)
            # train tuner
            tuner = tuner_dict["tuner"]
            tuner_name = tuner_dict["name"]

            print( tuner_name , "#"*50)

            timer = Timer()
            timer.start()
            tuner.fit(train_X,train_y)
            time = timer.get_time()
            estimator = tuner.best_estimator_
            best_params =  tuner.best_params_
            tuner_dict["estimator"] = estimator
            tuner_dict["params"] = best_params

            overal_train_error= estimator.error(train_X,train_y,plt=axs[0],name="train")
            tuner_dict["scores"] = {}
            tuner_dict["fit_time"] = time

            scores = tuner_dict["scores"]
            scores["train"] = overal_train_error["ratio"]

            axs_counter = 0
            for scenario_part_name, scenario_part in scenario_data.items():  # scenarios
                axs_counter += 1
                assert "injected" in scenario_part, print(scenario_part)
                validation_X , validation_y = scenario_part["injected"], scenario_part["original"]

                overal_train_error = estimator.error(validation_X, validation_y, plt=axs[axs_counter], name=scenario_part_name)

                scores[scenario_part_name] = overal_train_error["ratio"]
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

    # def plot(self, to_plot=None, prefix=""):
    #     to_plot = to_plot if to_plot is not None else ["time", "error"]
    #     to_plot = to_plot if isinstance(to_plot, list) else [to_plot]
    #     grouped = self.results.groupby("tuner")
    #     for attribute in to_plot:
    #         for (title, optimizer) in grouped:
    #             x = range(len(optimizer[attribute]))
    #             plt.plot(x, optimizer[attribute], label=title, marker="x")
    #         plt.xticks(x, optimizer["scenario_part"])
    #         plt.legend()
    #         plt.title(attribute)
    #         plt.savefig(f'ParameterTuning/{prefix}_{attribute}.svg')
    #         plt.clf()

    # def save(self, prefix=""):
    #     self.plot(prefix=prefix)
    #     # grouped = self.results.groupby("tuner")
    #     # self.results.to_dict('records')
    #     #
        # import toml
        #
        # output_file_name = "parammmmms.toml"
        # with open(output_file_name, "w") as toml_file:
        #     toml.dump(self.results.to_dict('records'), toml_file)

class GridSearch():
    def _iter_test_indices(self, X, y=None, groups=None):
        super()._iter_test_indices(X,y,groups)
        # n_samples = _num_samples(X)
        # indices = np.arange(n_samples)
        # if self.shuffle:
        #     check_random_state(self.random_state).shuffle(indices)
        #
        # n_splits = self.n_splits
        # fold_sizes = np.full(n_splits, n_samples // n_splits, dtype=int)
        # fold_sizes[: n_samples % n_splits] += 1
        # current = 0
        # for fold_size in fold_sizes:
        #     start, stop = current, current + fold_size
        #     yield indices[start:stop]
        #     current = stop
        for i in range(2):
            yield np.arange(X.shape[0])