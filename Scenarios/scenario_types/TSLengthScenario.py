import math

from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.ScenarioConfig import TS_LENGTH


class TSLengthScenario(BaseScenario):
    scenario_type = TS_LENGTH
    small_data_description = "TS length"


    def transform_df(self, df , cols = [0] ,seed = 100):
        result = {}
        data = df.copy()
        n,m = df.shape

        center= math.floor(n/2)
        fifteen_percent = math.floor(n/100*15)
        five_percent = math.floor(n/100*5)
        for col in cols:
            data.iloc[center-fifteen_percent:center+fifteen_percent,col] , _ = self.inject_single(data.iloc[center-fifteen_percent:center+fifteen_percent,col])

        for i in range(8):
            lower , upper = center-i*five_percent-fifteen_percent, center+i*five_percent+fifteen_percent
            result[f"{round(n/(upper-lower))}"] = self.create_scenario_part_output(data.iloc[lower:upper], df.iloc[lower:upper] , cols ,self.train)

        return result
