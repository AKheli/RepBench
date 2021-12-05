from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Injection.injection_methods.advanced_injections import inject_equal_spaced
from Scenarios.Scenario_Types import VARY_TS_LENGHT, scenario_specifications
from Scenarios.BaseScenario import BaseScenario
import numpy as np


class TSLengthScenario(BaseScenario):
    scenario_type = VARY_TS_LENGHT

    def __init__(self, anomaly_type=AMPLITUDE_SHIFT,
                 anomaly_percentage=None,
                 anomaly_length=None,
                 default_params=scenario_specifications[scenario_type],
                 ):
        self.anomaly_percentage = anomaly_percentage or default_params["anomaly_percentage"]
        self.anomaly_length = anomaly_length or default_params["anomaly_length"]
        self.anomaly_type = anomaly_type

    def inject_single(self, data):
        data = np.array(data)
        anomalies_per_block = int(self.get_amount_of_anomalies(data) / 10)
        data, info = inject_equal_spaced(data, anomaly_type=self.anomaly_type, n=10, location="random"
                                         , anomalies_per_block=anomalies_per_block,
                                         anomalylength=self.anomaly_length)
        return data, info

    def data_trasform(self, data):
        return [data.iloc[:int(i * 10 * len(data) / 100), :] for i in range(1, 11)]
