""" data_file -> dfs_to_be_evaluated , info  """
from Injection.res.Injector import Anomalygenerator
import numpy as np


class BaseScenario():
    def __init__(self, df, anomaly_type="amplitude_shift", col=0, anomaly_percentage=0.05, anomaly_length=15):
        anomaly_percentage = anomaly_percentage if anomaly_percentage < 1 else anomaly_percentage / 100
        assert anomaly_type in Anomalygenerator.anomalies.keys(), f"anomaly type {anomaly_type} not found , suppoeted are {Anomalygenerator.anomalies.keys()} else modify the injector file"

        self.anomaly_percentage = anomaly_percentage
        self.anomaly_type = anomaly_type
        self.anomaly_length = anomaly_length
        self.data = df
        self.to_inject = np.array(df.iloc[:, col])
        self.col = col

    def inject(self):
        data = np.array(self.to_inject)
        amount_of_anomalies = int(len(data) * self.anomaly_percentage / self.anomaly_length)
        generator = Anomalygenerator(data)
        generator.add_distortion(length = self.anomaly_length , number_of_ranges=amount_of_anomalies,use_param_file = False)
        return generator.get_injected_series()

    def get_scenario_info(self):
        return f"BaseScenario"



    def get_injected_data(self):
        data  = self.data.copy()
        data.iloc[:,self.col] = self.inject()
        cols = list(data.columns)
        name = cols[self.col]
        cols[self.col] = "injected"
        data.columns = cols
        return [{"data" : data, "truth" :np.array(self.to_inject) , "original_name": name , "scenario_info" : self.get_scenario_info(), "anomaly_type" : self.anomaly_type }]


#scenario anomaly datafile