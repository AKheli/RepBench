import numpy as np
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import ANOMALY_SIZE



##
class AnomalyLengthScenario(BaseScenario):
    scenario_type = ANOMALY_SIZE
    default_lengths = [5,10,15,20,50,100]


    def init_specialiced_scenario(self):
        self.lengths = self.default_lengths
        if max(self.lengths)*2+2 > len(self.original_test):
            print(f"Warning : ts ({len(self.original_test)},) to small for {self.lengths} anomaly sizes use update_lengths")


    def update_lengths(self,list):
        self.lengths = list



    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data)/max(self.lengths)/3)
        assert anom_amount >= 1 , f'{len(data)}'
        return anom_amount




    def transform_df(self, df, cols=[0]):
        data = df.copy()
        resulting_data = []
        result = {}
        x = self.anomaly_length
        for l in self.lengths:
            np.random.seed(100)
            self.anomaly_length = l
            injected_df = data.copy()
            for col in cols:
                    injected_df.iloc[:, col], anomaly_info = self.inject_single(np.array(data.iloc[:, col]),
                                                                            min_space_anom_len_multiplier=0)
            resulting_data.append(injected_df)
            result[f'anomaly_size{l}'] = self.create_scenario_part_output(injected_df, data, cols, self.train)
        self.anomaly_length = x
        return result


