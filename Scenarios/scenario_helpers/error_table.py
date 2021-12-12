import pandas as pd
from prettytable import PrettyTable



class RepairEvaluator:
    def __init__(self,save_path,scenario_type):
            self.save_path=save_path,
            self.rows = {}
            self.scenario_type = scenario_type


    def add(self,scenario_part,truth,injected,repairs,cols):
        self.rows[scenario_part] = { "truth" : truth , "injected" : injected
                                     ,"repairs" : repairs , "columns" : cols}



    def calculate_errors(self,truth,injected,repairs, error_func):
        errors = {"original_error" : error_func(truth,injected)}
        for algo_name , algo_output in repairs.items():
            errors[algo_name] = error_func(truth,algo_output["repair"] ,algo_output.get("labels" , None))
        return errors

    def generate_error_df(self,error_func):
        df= pd.DataFrame()
        for k,v in self.rows.items():
            truth = v["truth"]
            injected = v["injected"]
            df = df.append(self.calculate_errors(truth,injected,v["repairs"],df),name=k)
        return df


    def save_table(self,error_func):
        t = PrettyTable(self.generate_df(error_func))
        t.align = 'l'  # align left
        t.border = False

        return t





