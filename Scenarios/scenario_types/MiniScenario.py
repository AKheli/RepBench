from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_random_ranges
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.Scenario_Types import scenario_specifications, MINI_SCENARIO
from Scenarios.scenario_types.BaseScenario import BaseScenario
import numpy as np


class MiniScenario(BaseScenario):
    scenario_type = MINI_SCENARIO


    def get_amount_of_anomalies(self, data):
        return 1



    def transform_df(self, df, cols=[0]):
        self.anomaly_length = 6
        i = np.random.randint(20,len(df))
        df = df.iloc[i-20:i,:]
        data = df.copy()
        for col in cols:
            data.iloc[:, col], anomaly_infos = self.inject_single(np.array(data.iloc[:, col]))

        return {"small_set": self.create_scenario_part_output(data, df, cols)}
