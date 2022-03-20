import pandas as pd

from Repair.res.timer import Timer
from Scenarios.Anomaly_Types import *
import numpy as np
from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_anomaly_indices
from Scenarios.scenario_types.Scenario_Types import BASE_SCENARIO
from data_methods.Helper_methods import get_df_from_file


class BaseScenario:
    scenario_type = BASE_SCENARIO
    small_data_description = "data size"
    default_length = 12
    default_percentage = 7
    default_anomaly_type = AMPLITUDE_SHIFT

    def __init__(self, data, anomaly_dict: dict = None
                 , cols_to_inject=None
                 , train_test_split=0.5
                 , data_columns="all", data_name=None):
        self.set_anomaly_params(anomaly_dict)
        self.injected_columns = [0] if cols_to_inject is None else cols_to_inject
        self.train_test_split = train_test_split
        self.data_filename = data

        if isinstance(data, pd.DataFrame):
            self.original_data, self.data_name = data, data_name
        else:
            assert isinstance(data, str), "data must be string or DataFrame"
            self.original_data, self.data_name = get_df_from_file(data)
            self.data_name = self.data_name if data_name is None else data_name

        if data_columns != "all":
            self.original_data = pd.DataFrame(self.original_data.iloc[:, data_columns])
        self.generate_data(self.original_data)
        self.repairs = {}
        self.repair_names = []

    def set_anomaly_params(self, anomaly_dict=None):
        if anomaly_dict is None:
            anomaly_dict = {}
        assert all([k in ["anomaly_length", "anomaly_type", "anomaly_percentage"] for k in anomaly_dict.keys()])

        self.anomaly_type = anomaly_dict.get("anomaly_type", self.default_anomaly_type)
        self.anomaly_percentage = anomaly_dict.get("anomaly_percentage", self.default_percentage)
        self.anomaly_length = anomaly_dict.get("anomaly_length", self.default_length)

        assert isinstance(self.anomaly_type, str) and isinstance(self.anomaly_length, int), f'{self.anomaly_length},' \
                                                                                            f' {self.anomaly_type}'

    def generate_data(self, original_data):
        self.original_train, self.original_test = self.split_train_test(original_data, self.train_test_split)
        self.scenarios = self.transform_df(self.original_test, self.injected_columns, seed=100)

        self.train = BaseScenario.transform_df(self, self.original_train, self.injected_columns, seed=200)["full_set"]

        return self.train, self.scenarios

    @staticmethod
    def split_train_test(df, train_test_split):
        l = int(len(df) * train_test_split)
        return df.iloc[:l, :], df.iloc[l:, :]

    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data) * self.anomaly_percentage / 100 / self.anomaly_length)
        assert anom_amount >= 1
        return anom_amount

    ##### injection
    def inject_single(self, data, seed=100, min_space_anom_len_multiplier=2, factor=None):
        index_ranges = get_anomaly_indices(data, self.anomaly_length
                                           , number_of_ranges=self.get_amount_of_anomalies(data), seed=seed
                                           , min_space_anom_len_multiplier=min_space_anom_len_multiplier)
        anomaly_infos = []
        if self.anomaly_length == 6:
            print(index_ranges)
        for range_ in index_ranges:
            data, info = add_anomaly(anomaly_type=self.anomaly_type, data=data, index_range=range_, factor=factor)
            anomaly_infos.append(info)
        return data, anomaly_infos

    def transform_df(self, df, cols=[0], seed=100):
        data = df.copy()
        for col in cols:
            data.iloc[:, col], anomaly_infos = self.inject_single(np.array(data.iloc[:, col]), seed=seed)

        return {"full_set": self.create_scenario_part_output(data, df, cols)}

    def create_scenario_part_output(self, injected, original, cols):
        original = original.reset_index(drop=True)
        injected = injected.reset_index(drop=True)
        return {
            "injected": injected,
            "original": original.copy(),
            "class": self.get_class(injected, original),
            "columns": cols}

    @staticmethod
    def get_class(injected, original):
        """ generates common class where entries are different"""
        return original.ne(injected)

    ### after scenrio has been initialized
    def add_repair(self, scenario_part: str, repair_results, repair_name: str):
        assert scenario_part in self.scenarios.keys(), f'{scenario_part} not in {self.scenarios.keys()}'

        if scenario_part not in self.repairs.keys():
            self.repairs[scenario_part] = {}
        self.repairs[scenario_part][repair_name] = repair_results

        if repair_name not in self.repair_names:
            self.repair_names.append(repair_name)

    def optimize(self, tuner, name, plt=None):
        """
        Parameters
        ----------
        tuner e.g gridsearch CV with specified model and grid
        plt or axs

        Returns
        -------
        {"train_error" : overal_train_error ,
                "train_time" : time ,
                "params" : best_params,
                "estimator"  : estimator ,
                "scenario_errors" : dict of scenario scores}
        """

        train_X, train_y = self.train["injected"], self.train["original"]
        timer = Timer()
        timer.start()
        tuner.fit(train_X, train_y)
        time = timer.get_time()
        estimator = tuner.best_estimator_

        if hasattr(self, "last_estimator"):
            assert id(estimator) != id(self.last_estimator), f'{id(estimator)} {id(self.last_estimator)}'
        self.last_estimator = estimator

        best_params = tuner.best_params_

        overal_train_error = estimator.error(train_X, train_y, plt=plt, name="train")

        scenario_scores = {}
        for scenario_part_name, scenario_part in self.scenarios.items():
            validation_X, validation_y = scenario_part["injected"], scenario_part["original"]
            error = estimator.error(validation_X, validation_y)
            scenario_scores[scenario_part_name] = error

        results = {"train_error": overal_train_error,
                   "train_time": time,
                   "params": best_params,
                   "estimator": estimator,
                   "scenario_errors": scenario_scores}

        if not hasattr(self, "opt_results"):
            self.opt_results = {}
        self.opt_results[name] = results

        return results

    def injected_anomaly_indexes(self, scenario=0):
        scen_name = list(self.scenarios.keys())[scenario]
        scenario_part = self.scenarios[scen_name]
        class_ = scenario_part["class"]
        indexes = []
        current = []
        for i, c in enumerate(np.array(class_)):
            if any(c):
                current.append(i)
            if not any(c):
                if len(current) > 0:
                    indexes.append(current)
                    current = []
        return indexes

    def get_amount_of_part_scenarios(self):
        return len(self.scenarios)

    def i_get_scenario(self, index):
        scen_name = list(self.scenarios.keys())[index]
        scenario_part = self.scenarios[scen_name]
        return scenario_part
