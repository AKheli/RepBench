import pandas as pd
from Scenarios.scenario_types.BaseScenario import BaseScenario

class CustomScenario(BaseScenario):
    scenario_type = "custom"
    small_data_description = ""

    def __init__(self,data_name = "custom" , anomaly_type = "custom"):
        self.data_name = data_name
        self.anomaly_type = anomaly_type
        self.repairs = {}
        self.repair_names = []
        self.scenarios = {}

    def add_scenario_part(self ,  injected , truth ,name , cols = [0] ):
        injected, truth = pd.DataFrame(injected) , pd.DataFrame(truth)
        self.scenarios[name] = self.create_scenario_part_output(truth,injected, cols)

    def add_train(self,truth,injected , cols = [0]):
        self.train = self.create_scenario_part_output(truth,injected, cols)
