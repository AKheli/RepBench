import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import VARY_ANOMALY_SIZE



##
class AnomalyLengthScenario(BaseScenario):
    scenario_type = VARY_ANOMALY_SIZE
    default_lengths = [5,10,15,20,50]


    def init_specialiced_scenario(self):
        self.lengths = self.default_lengths
        if max(self.lengths)*2+2 > len(self.original_test):
            print(f"Warning : ts ({len(self.original_test)},) to small for {self.lengths} anomaly sized use update_lengths")

    def update_lengths(self,list):
        self.lengths = list





    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data)/max(self.lengths)*2)
        assert anom_amount >= 1 , f'{len(data)}'
        return anom_amount




    def transform_df(self, df, cols=[0],seed = 100):


        # todo check result appending
        for l in self.lengths:
            x = self.anomaly_length

        data = df.copy()
        resulting_data = []
        result = {}
        x = self.anomaly_length
        for l in self.lengths:
            self.anomaly_length = l
            injected_df = data.copy()
            for col in cols:
                injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            min_space_anom_len_multiplier=0)
            resulting_data.append(injected_df)
            result[f'anomaly_size{i}'] = self.create_scenario_part_output(injected_df, data, cols)
        self.anomaly_length = x
        return result


