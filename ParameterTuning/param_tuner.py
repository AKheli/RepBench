import pandas as pd
from matplotlib import pyplot as plt
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV, GridSearchCV
from skopt import BayesSearchCV

from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE


# tune a datset
# scenario tuner give scenario as parameter
class ParamTuner():
    def __init__(self, n_jobs=-1, error=RMSE, classification=False):
        self.parameter_tuners = []
        self.n_jobs = n_jobs
        self.results = []
        self.classification = classification
        self.error = error

    def init_tuner(self, tuner_name, param_grid, clf, tuner_params=None, cv=None):
        assert tuner_name.lower()[:2] in ["ba", "gr", "gs", "ha", "hg", "bc"], "tuner could not be passed"
        tuner_name = tuner_name.lower()[:2]
        if tuner_name in ["ba"]:
            return BayesianOptimization(clf, param_grid, n_jobs=self.n_jobs)
        if tuner_name in ["gr", "gs"]:
            return GridSearchCV(clf, param_grid, n_jobs=self.n_jobs , cv = cv)
        if tuner_name in ["bc"]:
            return BayesSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                 random_state=0 ,cv = cv)
        if tuner_name in ["ha", "hg"]:
            return HalvingGridSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0 ,cv = cv)

    def add(self, repair_estimator, param_grid, tuners: list,
            cv=None):  # tuner params
        if isinstance(param_grid, str):
            # param_grid = load_param_grid(param_grid)[algorithm_name]
            pass

        tuners = list(tuners if isinstance(tuners, list) else [tuners])
        for tuner in tuners:
            self.parameter_tuners.append({"tuner": self.init_tuner(tuner, param_grid, repair_estimator , cv =  cv)})

    def optimize_scenario(self, scenario):
        scenario_data = scenario["scenario_data"]

        train_X,train_y = scenario["train"] , scenario["train_original"]
        for tuner_dict in self.parameter_tuners:
            tuner = tuner_dict["tuner"]
            timer = Timer()
            timer.start()
            tuner.fit(train_X,train_y)
            time = timer.get_time()
            estimator = tuner.best_estimator_
            best_params =  tuner.best_params_

            overal_train_score = -estimator.score(train_X,train_y)
            original_train_score = -estimator.score(train_X,train_y,predict= False)
            tuner_results = [type(tuner).__name__ ,  best_params ,  ("time" ,  time) ,("original_train_score" , original_train_score), ("train_score", overal_train_score)]
            for scenario_part_name, scenario_part in scenario_data.items():  # scenarios
                assert "injected" in scenario_part, print(scenario_part)
                validation_X , validation_y = scenario_part["injected"], scenario_part["original"]
                tuner_results.append(("original_error",-estimator.score(validation_X, validation_y, predict = False)))

                #validation_y.plot()
                #plt.title("y")
                #plt.show()
                #validation_X.plot()
                #plt.title("X")
                #plt.show()
                part_scenario_score = -estimator.score(validation_X, validation_y)
                tuner_results.append(("pref_fit",part_scenario_score))

                # pd.DataFrame(estimator.predict(validation_X)).plot()
                # plt.title("prefit")
                #plt.show()

                estimator.fit(validation_X) #todo
                #pd.DataFrame(estimator.predict(validation_X)).plot()
                #plt.show()
                part_scenario_score = -estimator.score(validation_X, validation_y)
                tuner_results.append(("refitted_fit",part_scenario_score ))
            print(tuner_results)
            self.results.append(tuner_results)


    # def search_param(self, train_X,train_y, ):  # injected , original or class
    #     train_X = injected.copy()
    #     train_y = truth
    #     search_results = []
    #     original_rmse = RMSE(injected, truth, [0])
    #
    #     for tuner_dict in self.parameter_tuners:
    #         tuner = self.update_tuner(tuner_dict,train_X,train_y)
    #         print(tuner.cv)
    #         print("starting", type(tuner).__name__)
    #         timer = Timer()
    #         timer.start()
    #         tuner.fit(injected, truth)
    #
    #         time = timer.get_time()
    #         best_params = tuner.best_params_
    #         estimator = tuner.best_estimator_
    #         estimator.fit(injected)
    #         original_error = self.error(injected, truth, [0])
    #
    #         error = estimator.score(injected, truth)
    #         search_results.append({"tuner": type(tuner).__name__,
    #                                "best_params": best_params,
    #                                "error": error,
    #                                # "error_normalized": round(error/original_error,3),
    #                                "error_name": self.error.__name__,
    #                                "time": time})
    #
    #     return search_results

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
