import numpy as np
from matplotlib import pyplot as plt

from Injection.injection_methods.basic_injections import add_anomaly
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import VARY_ANOMALY_SIZE, scenario_specifications, ANOMALY_FACTOR


class AnomalyFactorScenario(BaseScenario):
    scenario_type = ANOMALY_FACTOR

    # def __init__(self, anomaly_type=AMPLITUDE_SHIFT,
    #              default_params=scenario_specifications[scenario_type]):

    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data)/100/3)
        assert anom_amount >= 1 , f'{len(data)}'
        return anom_amount

    # todo for multiple series injected the center migh not be ideal
    # def inject_single(self, data):
    #     data = np.array(data)
    #     index_range = get_center(len(data), self.anomaly_length)
    #     anomaly_infos = []
    #     data, info = add_anomaly(anomaly_type=self.anomaly_type, data=data, index_range=index_range)
    #     return data , info

    def transform_df(self, df, cols=[0]):
        data = df.copy()
        resulting_data = []
        result = {}
        for i in [1,5,10,15,20,30,40,50,100,200]:
            self.factor = i
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            min_space_anom_len_multiplier=0,factor=i)
            injected_df.plot()
            plt.show()
            resulting_data.append(injected_df)
            result[f'anomaly_factor{i}'] = self.create_scenario_part_output(injected_df, data, cols)

        return result


