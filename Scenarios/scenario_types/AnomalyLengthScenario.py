import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import VARY_ANOMALY_SIZE


class AnomalyLengthScenario(BaseScenario):
    scenario_type = VARY_ANOMALY_SIZE

    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data)/300)
        assert anom_amount >= 1 , f'{len(data)}'
        return anom_amount

    def transform_df(self, df, cols=[0],seed = 100):
        data = df.copy()
        resulting_data = []
        result = {}
        x = self.anomaly_length
        for i in [10*i for i in range(1,11)]:
            self.anomaly_length = i
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            min_space_anom_len_multiplier=0)
            resulting_data.append(injected_df)
            result[f'anomaly_size{i}'] = self.create_scenario_part_output(injected_df, data, cols)
        self.anomaly_length = x
        return result


