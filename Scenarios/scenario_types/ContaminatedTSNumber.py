##
import pandas as pd
from matplotlib import pyplot as plt

from Scenarios.scenario_types.BaseScenario import BaseScenario
import numpy as np
from Scenarios.scenario_types.ScenarioConfig import CTS_NBR


class ContaminatedNumberOfTSScenario(BaseScenario):
    scenario_type = CTS_NBR
    small_data_description = "infected TS #"

    def transform_df(self, df, cols=None, seed=0):
        fully_injected = df.copy()

        ## create fully contaminated series
        for col in range(df.shape[1]):  ## inject all
            np.random.seed(col)
            fully_injected.iloc[:, col], anomaly_infos = self.inject_single(np.array(fully_injected.iloc[:, col]))

        ## create list witn amount of contaminated series
        max_contamination = fully_injected.shape[1]
        contaminated_series = [n for n in self.contaminated_ts if n <= max_contamination]
        if max_contamination not in contaminated_series:
            contaminated_series.append(max_contamination)

        result = {}
        for l in contaminated_series:
            injected = df.copy()
            assert isinstance(l,int) ,\
                f'{l} in {contaminated_series} generated from {self.contaminated_ts} could not index dataframe"'

            injected.iloc[:, :l] = fully_injected.iloc[:, :l].copy()

            result[f"{l}"] = self.create_scenario_part_output(
                injected, df,
                list(range(l)), self.train)

        return result
