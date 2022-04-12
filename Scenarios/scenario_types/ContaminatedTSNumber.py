##
import pandas as pd
from Scenarios.scenario_types.BaseScenario import BaseScenario
import numpy as np
from Scenarios.scenario_types.ScenarioConfig import CTS_NBR


class ContaminatedNumberOfTSScenario(BaseScenario):
    scenario_type = CTS_NBR
    default_numbers = [1,2,3,5,7,10,15,20,30,40,50]


    def init_specialiced_scenario(self):
        self.number_of_ts = self.default_numbers
        self.single_train = False

    def transform_df(self, df, cols=[0],seed=0):
        data = df.copy()

        for col in range(df.shape[1]): ## inject all
            np.random.seed(col)
            data.iloc[:, col], anomaly_infos = self.inject_single(np.array(data.iloc[:, col]))

        result = {}
        for l in set([n for n in self.number_of_ts if n <= data.shape[1]]+[df.shape[1]]):
            injected = df.copy()
            injected[:l] = data.copy()[:l]

            result[f"ts_number{l}"] = self.create_scenario_part_output(
                injected, df,
                list(range(l)),self.train)
        return result