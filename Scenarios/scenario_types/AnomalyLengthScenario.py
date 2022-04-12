import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.ScenarioConfig import ANOMALY_SIZE


class AnomalyLengthScenario(BaseScenario):
    scenario_type = ANOMALY_SIZE

    @property
    def anomaly_length(self):
        """
        overwritten for training
        anomaly size is updated in transform_df
        """
        if not hasattr(self, "anomaly_size"):
            return int(self.n_cols * self.anomaly_sizes[3] / 100)
        return int(self.n_cols * self.anomaly_size / 100)

    def get_amount_of_anomalies(self):
        anom_amount = round(self.anomaly_percentage / self.anomaly_sizes[0])
        assert anom_amount >= 1
        return anom_amount

    def transform_df(self, df, cols=[0], seed=100):
        print("AAAAAAAA")
        data = df.copy()
        resulting_data = []
        result = {}
        for size in self.anomaly_sizes:
            np.random.seed(100)
            self.anomaly_size = size
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            min_space_anom_len_multiplier=0)
            resulting_data.append(injected_df)
            result[f'anomaly_size: {size}%'] = self.create_scenario_part_output(injected_df, data, cols, self.train)
        return result
