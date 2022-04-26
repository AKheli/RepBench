import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.ScenarioConfig import ANOMALY_RATE


class AnomalyRateScenario(BaseScenario):
    scenario_type = ANOMALY_RATE
    small_data_description = "anomaly %"
    # @property
    # def anomaly_length(self):
    #     """
    #     overwritten for training
    #     anomaly size is updated in transform_df
    #     """
    #     if not hasattr(self, "anomaly_size"):
    #         return int(self.n_cols * self.anomaly_sizes[3] / 100)
    #     return int(self.n_cols * self.anomaly_size / 100)
    #
    # def get_amount_of_anomalies(self):
    #     anom_amount = round(self.anomaly_percentage / self.anomaly_sizes[0])
    #     assert anom_amount >= 1
    #     return anom_amount

    def get_amount_and_length(self, counter=2):
        l = self.a_length
        n = self.n_rows
        p = self.a_percentages[counter]
        anom_amount = round(n / 100 / l * p)
        if anom_amount == 0:
            return 1 , round(l/2)
        return anom_amount, l

    def transform_df(self, df, cols=[0], seed=100):
        data = df.copy()
        resulting_data = []
        result = {}
        for c,_ in enumerate(self.a_percentages):
            amount, length = self.get_amount_and_length(counter=c)
            np.random.seed(100)
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            anomaly_length = length,
                                                                            anomaly_amount= amount,
                                                                            min_space_anom_len_multiplier=0)
            resulting_data.append(injected_df)
            result[amount] = self.create_scenario_part_output(injected_df, data, cols, self.train)
        return result
