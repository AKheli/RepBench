import pandas as pd

from Repair.res.timer import Timer
from Scenarios.Anomaly_Types import *
import numpy as np
from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_anomaly_indices
from Scenarios.scenario_types.ScenarioConfig import *
from data_methods.Helper_methods import get_df_from_file


class BaseScenario:
    scenario_type = BASE_SCENARIO
    small_data_description = "data size"
    default_length = 12
    default_percentage = 7
    default_anomaly_type = AMPLITUDE_SHIFT

    def __init__(self, data
                 , cols_to_inject=None
                 , train_test_split=0.5
                 , train = None
                 , data_name=None , **kwargs ):


        self.data_name = data_name
        self.single_train = True
        self.set_anomaly_params(**kwargs)
        self.injected_columns = [0] if cols_to_inject is None else cols_to_inject
        self.train_test_split = train_test_split
        self.data_filename = data


        ### get train and test split
        self.read_data_into_train_and_test(data,train_test_split,train)


        assert hasattr(self,"original_test") and hasattr(self,"original_train")
        self.init_specialiced_scenario()
        self.generate_data()

        self.repairs = {}
        self.repair_names = []



    def read_data_into_train_and_test(self, data , train_test_split = 0.5 , train = None):
        if isinstance(data, pd.DataFrame):
            original_data = data
        else:
            assert isinstance(data, str), "data must be string or DataFrame"
            original_data, data_name = get_df_from_file(data)
            if self.data_name is None:
                self.data_name = data_name

        if train is not None:
            if isinstance(data, pd.DataFrame):
                self.original_train = train
            else:
                assert isinstance(data, str), "data must be string or DataFrame"
                self.original_train, _ = get_df_from_file(data)
            self.original_test = original_data

        else:
            self.original_train ,self.original_test = self.split_train_test(original_data,train_test_split)
        self.n_cols = self.original_test.shape[0]

    def init_specialiced_scenario(self):
        pass


    @property
    def name_train_test_iter(self):
        return iter( [(name,scen_part["train"],scen_part) for name, scen_part in self.scenarios.items()])


    def set_anomaly_params(self , **kwargs):
        self.anomaly_type = self.default_anomaly_type
        self.__dict__.update(scenario_specifications[self.scenario_type])
        for name in kwargs.keys():
            assert name in self.__dict__ , f'{name} is not a valid parameter'
        self.__dict__.update(**kwargs)


    def generate_data(self):
        self.train = None # needed such that the trian of train is None
        self.train = BaseScenario.transform_df(self, self.original_train, self.injected_columns, seed=200)["full_set"]
        self.scenarios = self.transform_df(self.original_test, self.injected_columns)
        return self.train, self.scenarios

    @staticmethod
    def split_train_test(df, train_test_split):
        if train_test_split == 0:
            return None , df

        l = int(len(df) * train_test_split)
        return df.iloc[:l, :], df.iloc[l:, :]

    @property
    def anomaly_length(self):
        return int(self.n_cols*self.anomaly_size/100)

    def get_amount_of_anomalies(self):
        anom_amount = round(self.anomaly_percentage / self.anomaly_size)
        assert anom_amount >= 1
        return anom_amount

    def inject_single(self, data, min_space_anom_len_multiplier=2, factor=None):
        index_ranges = get_anomaly_indices(data, self.anomaly_length
                                           , number_of_ranges=self.get_amount_of_anomalies()
                                           , min_space_anom_len_multiplier=min_space_anom_len_multiplier)
        anomaly_infos = []
        assert len(index_ranges) != 0
        for range_ in index_ranges:
            assert len(range_) != 0
            data, info = add_anomaly(anomaly_type=self.anomaly_type, data=data, index_range=range_, factor=factor)
            anomaly_infos.append(info)
        return data, anomaly_infos

    def transform_df(self, df, cols=[0],seed=100):
        np.random.seed(seed)
        data = df.copy()
        for col in cols:
            data.iloc[:, col], anomaly_infos = self.inject_single(np.array(data.iloc[:, col]))

        return {"full_set": self.create_scenario_part_output(data, df, cols ,self.train)}

    def create_scenario_part_output(self, injected, original, cols , train = None):
        original = original.reset_index(drop=True)
        injected = injected.reset_index(drop=True)
        truth = original.copy()
        return {
            "injected": injected,
            "original": truth,
            "truth" : truth,
            "class": self.get_class(injected, original),
            "columns": cols,
            "train": train,
        }

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


