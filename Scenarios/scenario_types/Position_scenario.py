from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.ScenarioConfig import ANOMALY_POSITION


class AnomalyPositionScenario(BaseScenario):
    scenario_type = ANOMALY_POSITION
    small_data_description = " "
    seeds = [1,2,3,4,5,6,7,8,9,10]

    def transform_df(self, df, cols=[0]):
        results = {}
        for i,seed in enumerate(self.seeds):
            results[f"{i}"] =  super().transform_df(df,cols,seed=seed)["full_set"]

        return results
