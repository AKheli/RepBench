from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Injection.injection_methods.advanced_injections import inject_equal_spaced
from Scenarios.Scenario_Types import VARY_TS_LENGTH, scenario_specifications
from Scenarios.BaseScenario import BaseScenario
import numpy as np


class TSLengthScenario(BaseScenario):
    scenario_type = VARY_TS_LENGTH
    small_data_description = "ts lenght"


    def __init__(self, anomaly_type=AMPLITUDE_SHIFT,
                 anomaly_percentage=None,
                 anomaly_length=None,
                 default_params=scenario_specifications[scenario_type],
                 ):
        self.anomaly_percentage = anomaly_percentage or default_params["anomaly_percentage"]
        self.anomaly_length = anomaly_length or default_params["anomaly_length"]
        self.anomaly_type = anomaly_type
        self.splits = 10

    def inject_single(self, data):
        data = np.array(data)
        anomalies_per_block = int(self.get_amount_of_anomalies(data) / self.splits)
        anomalies_per_block = max(anomalies_per_block,1)
        data, info = inject_equal_spaced(data, anomaly_type=self.anomaly_type, n=self.splits, location="random"
                                         , anomalies_per_block=anomalies_per_block,
                                         anomalylength=self.anomaly_length)
        return data, info

    def transform_df(self, df , cols = [0]):
        result = {}
        data = df.copy()

        for col in cols:
            data.iloc[:,col] , _ = self.inject_single(data.iloc[:,col])

        for i in range(1,self.splits+1):
            length = int(i * self.splits * len(data) / 100)
            result[f"{length}"] = self.create_dict(data.iloc[:length] , df.iloc[:length])

        return result
