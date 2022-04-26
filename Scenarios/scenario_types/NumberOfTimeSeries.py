##
import pandas as pd

from Scenarios.scenario_types.BaseScenario import BaseScenario
import numpy as np

from Scenarios.scenario_types.ScenarioConfig import TS_NBR


class NumberOfTSScenario(BaseScenario):
    scenario_type = TS_NBR
    default_numbers = [3,5,7,10,15,20,30,40,50]
    small_data_description = "TS #"




    def init_specialiced_scenario(self):
        self.number_of_ts = self.default_numbers
        self.single_train = False

    def transform_df(self, df,seed=100):
        np.random.seed(seed)
        data = df.copy()
        cols = self.injected_columns
        anom_amount, anom_length = self.get_amount_and_length()

        for col in cols:
            data.iloc[:, col], anomaly_infos =\
                self.inject_single(np.array(data.iloc[:, col]),anomaly_length = anom_length,anomaly_amount=anom_amount)

        result = {}
        for l in [n for n in self.number_of_ts if n <= data.shape[1]] :
            injected_part = data.iloc[:,:l]
            original_part = df.iloc[:,:l]
            train_part = {}
            for key ,v in self.train.items():
                train_part[key] = v.iloc[:,:l] if isinstance(v,pd.DataFrame) else v

            cols_part  = [c for c in cols if c < l]
            result[l] = self.create_scenario_part_output(
                injected_part, original_part,
                cols_part , train_part)
        return result