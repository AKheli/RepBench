from Scenarios.Anomaly_Types import *
import numpy as np
from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_random_ranges
from Scenarios.Scenario_Types import BASE_SCENARIO, scenario_specifications


class BaseScenario():
    scenario_type = BASE_SCENARIO

    def __init__(self, anomaly_type = AMPLITUDE_SHIFT ,
                 anomaly_percentage = None,
                 anomaly_length = None,
                 default_params = scenario_specifications[scenario_type]):

        self.anomaly_percentage = anomaly_percentage or default_params["anomaly_percentage"]
        self.anomaly_length = anomaly_length or default_params["anomaly_length"]
        self.anomaly_type = anomaly_type

    def get_amount_of_anomalies(self,data):
        return int(len(data) * self.anomaly_percentage / self.anomaly_length)

    def inject_single(self, data):
        data = np.array(data)
        index_ranges = get_random_ranges(data,self.anomaly_length, number_of_ranges=self.get_amount_of_anomalies(data))
        anomaly_infos = []
        for range_ in index_ranges:
            data , info = add_anomaly(anomaly_type=self.anomaly_type , data=data ,index_range= range_)
            anomaly_infos.append(info)
        return data , anomaly_infos

    def data_trasform(self,data):
        return [data]

    def transform_df(self, df, cols=[0]):
        data = df.copy()
        for col in cols:
            data.iloc[:, col]  , anomaly_infos = self.inject_single(np.array(data.iloc[:, col]))

        resulting_data = self.data_trasform(data)
        assert isinstance(resulting_data, list)
        return {"injected_data": resulting_data, "anomaly_type": self.anomaly_type , "anomaly_infos" : [anomaly_infos]}




