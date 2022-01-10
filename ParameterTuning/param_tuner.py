
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV, GridSearchCV
from skopt import BayesSearchCV

from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE


class ParamTuner():
    def __init__(self, n_jobs=-1, error = RMSE , classification = False):
        self.parameter_tuners = []
        self.n_jobs = n_jobs
        self.results = pd.DataFrame()
        self.classification = classification
        self.error = error

    def init_tuner(self, tuner_name, param_grid, clf, tuner_params=None):
        assert tuner_name.lower()[:2] in ["ba", "gr", "gs", "ha", "hg", "bc"], "tuner could not be passed"
        tuner_name = tuner_name.lower()[:2]
        if tuner_name in ["ba"]:
            return BayesianOptimization(clf, param_grid, n_jobs=self.n_jobs)
        if tuner_name in ["gr", "gs"]:
            return GridSearchCV(clf, param_grid, n_jobs=self.n_jobs)
        if tuner_name in ["bc"]:
            return BayesSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0)
        if tuner_name in ["ha", "hg"]:
            return HalvingGridSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0)

    def add(self, repair_estimator, param_grid, tuners: list, tuner_parameters=None):
        if isinstance(tuner_parameters, str):  # toml file
            # param_grid = load_param_grid(tuner_parameters)[tuner_parameters]
            pass
        if isinstance(param_grid, str):
            # param_grid = load_param_grid(param_grid)[algorithm_name]
            pass

        tuners = list(tuners if isinstance(tuners, list) else [tuners])
        for tuner in tuners:
            self.parameter_tuners.append(self.init_tuner(tuner, param_grid, repair_estimator))

    def optimize_scenario_data(self, scenario_data):
        if "scenario_data" in scenario_data:
            scenario_data = scenario_data["scenario_data"]

        for scenario_part_name, scenario_part in scenario_data.items():  # scenarios
            assert "injected" in scenario_part, print(scenario_part)
            truth = scenario_part["original"] if not self.classification else scenario_part["class"]
            result = self.search_param(scenario_part["injected"],truth)

            for r in result:
                r.update( {"scenario_part" : scenario_part_name})

                self.results = self.results.append(pd.Series(r), ignore_index=True)


    def search_param(self, injected,truth):  # injected , original or class
        injected = injected.copy()
        search_results = []
        original_rmse = RMSE(injected, truth, [0])

        for tuner in self.parameter_tuners:
            print("starting",type(tuner).__name__)
            timer = Timer()
            timer.start()
            tuner.fit(injected, truth)

            time = timer.get_time()
            best_params = tuner.best_params_
            estimator = tuner.best_estimator_
            estimator.fit(injected)
            original_error = self.error(injected, truth, [0])

            error = estimator.score(injected,truth)
            search_results.append({ "tuner" :type(tuner).__name__,
                                    "best_params" : best_params,
                                    "error" : error ,
                                    #"error_normalized": round(error/original_error,3),
                                    "error_name": self.error.__name__,
                                    "time" : time})

        return search_results

    def plot(self,to_plot = None , prefix=""):
        to_plot = to_plot if to_plot is not None else ["time","error"]
        to_plot = to_plot if  isinstance(to_plot,list) else [to_plot]
        grouped = self.results.groupby("tuner")
        for attribute in to_plot:
            for (title,optimizer) in grouped:
                x = range(len(optimizer[attribute]))
                plt.plot(x, optimizer[attribute], label=title, marker="x")
            plt.xticks(x, optimizer["scenario_part"])
            plt.legend()
            plt.title(attribute)
            plt.savefig(f'ParameterTuning/{prefix}_{attribute}.svg')

    def save(self,prefix=""):
        self.plot(prefix=prefix)
        # grouped = self.results.groupby("tuner")
        # self.results.to_dict('records')
        #
        # import toml
        #
        # output_file_name = "parammmmms.toml"
        # with open(output_file_name, "w") as toml_file:
        #     toml.dump(self.results.to_dict('records'), toml_file)
