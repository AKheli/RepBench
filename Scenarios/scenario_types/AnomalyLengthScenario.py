import numpy as np

from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_center
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import VARY_ANOMALY_SIZE, scenario_specifications


class AnomalyLengthScenario(BaseScenario):
    scenario_type = VARY_ANOMALY_SIZE

    def __init__(self, anomaly_type=AMPLITUDE_SHIFT,
                 anomaly_length_start=None,
                 anomaly_length_step=None,
                 default_params=scenario_specifications[scenario_type]):

        self.anomaly_length_start = anomaly_length_start or default_params["anomaly_length_start"]
        self.anomaly_length_step = anomaly_length_step or default_params["anomaly_length_step"]
        self.anomaly_type = anomaly_type

    def get_amount_of_anomalies(self, data):
        return 1

    # todo for multiple series injected the center migh not be ideal
    def inject_single(self, data):
        data = np.array(data)
        index_range = get_center(len(data), self.anomaly_length)
        anomaly_infos = []
        data, info = add_anomaly(anomaly_type=self.anomaly_type, data=data, index_range=index_range)
        return data , info

    def transform_df(self, df, cols=[0]):
        data = df.copy()
        self.anomaly_length = self.anomaly_length_start
        resulting_data = []
        anomaly_infos = []
        for i in range(10):
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]))
                anomaly_infos.append(anomaly_info) # todo

            resulting_data.append(injected_df)
            self.anomaly_length = self.anomaly_length + self.anomaly_length_step

        assert isinstance(resulting_data, list)
        return {"injected_data": resulting_data, "anomaly_type": self.anomaly_type, "anomaly_infos": [anomaly_infos]}


