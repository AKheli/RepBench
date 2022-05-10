import math

import numpy as np

from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.ScenarioConfig import TS_LENGTH


class TSLengthScenario(BaseScenario):
    scenario_type = TS_LENGTH
    small_data_description = "TS length %"

    def get_amount_and_length(self, counter=0):
        l = self.a_length
        n = self.n_rows
        p = self.a_percentage/2
        anom_amount = round(n / 100 / l * p)
        return anom_amount, l


    def transform_df(self, df , cols = [0] ,seed = 100):
        np.random.seed(seed)
        cols = self.injected_columns
        anom_amount, anom_length = self.get_amount_and_length()
        result = {}

        data = df.copy()
        n,m = df.shape
        center= math.floor(n/2)
        fifteen_percent = math.floor(n/100*15)
        five_percent = math.floor(n/100*5)
        #assert False, data.iloc[center-fifteen_percent:center+fifteen_percent,cols]
        for col in cols:
            data.iloc[center-fifteen_percent:center+fifteen_percent,col] , _ = \
                self.inject_single(data.iloc[center-fifteen_percent:center+fifteen_percent,col],
                                   anomaly_length = anom_length,anomaly_amount=anom_amount)

        for i in range(8):
            lower , upper = center-i*five_percent-fifteen_percent, center+i*five_percent+fifteen_percent
            result[round(100*(upper-lower)/n)] = self.create_scenario_part_output(data.iloc[lower:upper], df.iloc[lower:upper] , cols ,self.train)
            print(result[round(100*(upper-lower)/n)]["class"])
            assert result[round(100*(upper-lower)/n)]["class"].any(None)

        return result
