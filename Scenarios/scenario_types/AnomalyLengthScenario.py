import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.ScenarioConfig import ANOMALY_SIZE


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

    def get_amount_and_length(self, counter=0):
        l = self.a_lengths[counter]
        n = self.n_rows
        p = self.a_percentage
        anom_amount = round(n / 100 / 10 * p)
        return anom_amount, l

    def transform_df(self, df,seed=100):
        np.random.seed(seed)
        data = df.copy()
        cols = self.injected_columns
        result = {}
        for c in range(len(self.a_lengths)):
            amount , length =  self.get_amount_and_length( counter=c)
            np.random.seed(100)
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            anomaly_length = length,
                                                                            anomaly_amount=amount,
                                                                            min_space_anom_len_multiplier=0.5)
            #resulting_data.append(injected_df)
            result[f'anomaly length: {length}'] = self.create_scenario_part_output(injected_df, data, cols, self.train)
        return result
