import pandas as pd
import toml
from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV

from Injection.inject import get_scenario_data, scenario_inject
from ParameterTuning.sklearn_bayesian import bayesian_opt, BayesianOptimization
from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.metrics import RMSE
from Scenarios.scenario_types.Scenario_Types import BASE_SCENARIO, VARY_TS_LENGTH
from data_methods.Helper_methods import get_df_from_file

injection_scenario = VARY_TS_LENGTH
# parameter_tuning = [bayesian_optimization,halving_grid_search,grid_search]

anomaly_type = AMPLITUDE_SHIFT
data_files = ["YAHOO.csv"]


class ParamTuner():
    def __init__(self, n_jobs=1):
        self.parameter_tuners = []
        self.n_jobs = n_jobs
        self.results = {}

    def init_tuner(self, tuner_name, param_grid, clf, tuner_params=None):
        print("name", tuner_name, type(tuner_name))
        assert tuner_name.lower()[:2] in ["ba", "gr", "gs", "ha", "hg"], "tuner could not be passed"
        tuner_name = tuner_name.lower()[:2]
        if tuner_name in ["ba"]:
            return BayesianOptimization(clf, param_grid, n_jobs=self.n_jobs)
        if tuner_name in ["gr", "gs"]:
            pass
        if tuner_name in ["ha", "hg"]:
            return HalvingGridSearchCV(clf, param_grid, n_jobs=self.n_jobs,
                                       random_state=0, scoring="neg_root_mean_squared_error")

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
        search_results = {}
        if "scenario_data" in scenario_data:
            scenario_data = scenario_data["scenario_data"]

        for scenario_part_name, scenario_part in scenario_data.items():  # scenarios
            assert "injected" in scenario_part, print(scenario_part)
            result = self.search_param(scenario_part["injected"],
                                       scenario_part["original"])
            search_results[scenario_part_name] = result
        self.results["name"] = search_results

    def search_param(self, injected, truth):  # X , y, repairfunction
        injected = injected.copy()
        search_results = {}
        for tuner in self.parameter_tuners:
            search_results[tuner] = {}
            tuner.fit(injected, truth)
            best_params = tuner.best_params_
            search_results[tuner] = {"best_params" : best_params}
            estimator = tuner.best_estimator_
            estimator.__dict__.update(best_params)
            estimator.fit(injected)
            rmse = RMSE(truth,pd.DataFrame(estimator.predict(injected)),[0])
            search_results[tuner] = {"best_params" : best_params, "rmse" : rmse}

        return search_results


param_grid = {
    # "threshold": np.arange(0.5, 3., 0.2),
    "n_components": [1, 2, 3]  # , 4, 5, 6],
    # "delta": [0.5 ** i for i in range(11)],
    # "component_method": ["TruncatedSVD"]
}
param_tuner = ParamTuner()
param_tuner.add(Robust_PCA_estimator(cols=[0, 1]), tuners=["ba", "ha"], param_grid=param_grid)
for file_name in data_files:
    df, name = get_df_from_file(file_name)
    scenario_data = scenario_inject(df, injection_scenario, anomaly_type)
    param_tuner.optimize_scenario_data(scenario_data)
