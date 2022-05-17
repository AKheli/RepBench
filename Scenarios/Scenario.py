import pandas as pd

import Scenarios.AnomalyConfig as ac
from Scenarios.scenario_generator import generate_scenario_data

class Scenario:
    def __init__(self, scen_name , data , a_type
                 , cols_to_inject=None
                 , train_test_split=0.5):

        assert a_type in ac.ANOMALY_TYPES

        self.a_type = a_type
        self.scen_name  = scen_name
        self.data_name = data.split(".")[0]
        self.part_scenarios = generate_scenario_data(scen_name,data,a_type,cols_to_inject,train_test_split,)

    @property
    def name_train_test_iter(self):
        return iter( [ (name , scen_part.train , scen_part ) for name, scen_part in self.part_scenarios.items()])

    def get_amount_of_part_scenarios(self):
        return len(self.part_scenarios)

    def metrics_df(self):
        d = {}
        for name , part in  self.part_scenarios.items():
            d[name] =  part.repairs

        d = pd.DataFrame.from_dict(d, orient='index')
        d.index.name = self.scen_name

        return d

    @property
    def repair_names(self):
        print( self.part_scenarios)
        return set(sum([p.repair_names for k,p in self.part_scenarios.items()],[]))














    # def optimize(self, tuner, name, plt=None):
    #     """
    #     Parameters
    #     ----------
    #     tuner e.g gridsearch CV with specified model and grid
    #     plt or axs
    #
    #     Returns
    #     -------
    #     {"train_error" : overal_train_error ,
    #             "train_time" : time ,
    #             "params" : best_params,
    #             "estimator"  : estimator ,
    #             "scenario_errors" : dict of scenario scores}
    #     """
    #
    #     train_X, train_y = self.train["injected"], self.train["original"]
    #     timer = Timer()
    #     timer.start()
    #     tuner.fit(train_X, train_y)
    #     time = timer.get_time()
    #     estimator = tuner.best_estimator_
    #
    #     if hasattr(self, "last_estimator"):
    #         assert id(estimator) != id(self.last_estimator), f'{id(estimator)} {id(self.last_estimator)}'
    #     self.last_estimator = estimator
    #
    #     best_params = tuner.best_params_
    #
    #     overal_train_error = estimator.error(train_X, train_y, plt=plt, name="train")
    #
    #     scenario_scores = {}
    #     for scenario_part_name, scenario_part in self.scenarios.items():
    #         validation_X, validation_y = scenario_part["injected"], scenario_part["original"]
    #         error = estimator.error(validation_X, validation_y)
    #         scenario_scores[scenario_part_name] = error
    #
    #     results = {"train_error": overal_train_error,
    #                "train_time": time,
    #                "params": best_params,
    #                "estimator": estimator,
    #                "scenario_errors": scenario_scores}
    #
    #     if not hasattr(self, "opt_results"):
    #         self.opt_results = {}
    #     self.opt_results[name] = results
    #
    #     return results
