from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Types import TS_LENGTH


class TSLengthScenario(BaseScenario):
    scenario_type = TS_LENGTH
    small_data_description = "TS length"


    def set_anomaly_params(self,anomaly_dict = None):
        if anomaly_dict is None:
            anomaly_dict = {}
        assert all([k in ["anomaly_length","anomaly_type","anomaly_percentage"] for k in anomaly_dict.keys()])

        self.anomaly_type = anomaly_dict.get("anomaly_type",self.default_anomaly_type)
        self.anomaly_percentage = anomaly_dict.get("anomaly_percentage",self.default_percentage)
        self.anomaly_length = anomaly_dict.get("anomaly_length",self.default_length)
        self.splits = 10

        assert isinstance(self.anomaly_type,str) and isinstance(self.anomaly_length,int) , f'{self.anomaly_length},' \
                                                                                           f' {self.anomaly_type}'
    def transform_df(self, df , cols = [0] ,seed = 100):
        result = {}
        data = df.copy()

        for col in cols:
            data.iloc[:,col] , _ = self.inject_single(data.iloc[:,col])

        for i in range(1,self.splits+1):
            length = int(i * self.splits * len(data) / 100)
            result[f"{length}"] = self.create_scenario_part_output(data.iloc[:length], df.iloc[:length] , cols ,self.train)

        return result
