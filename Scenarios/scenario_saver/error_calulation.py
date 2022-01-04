import pandas as pd

from Repair.Algorithms_File import ALGORITHM_COLORS
from Scenarios.metrics import *
from itertools import cycle
import os

def calculate_errors( truth, injected, repairs, columns , error_func):
    errors = {"original_error": error_func(truth, injected, columns)}
    for algo_name, algo_output in repairs.items():
        errors[algo_name] = error_func(truth, algo_output["repair"],columns, algo_output.get("labels", None))
    return errors

def generate_error_df(values,  error_func):
    df = pd.DataFrame()
    for k, v in values.items():
        truth = v.get("truth",None) if v.get("truth",None) is not None else v.get("original",None)
        assert truth is not None
        injected = v["injected"]
        df = df.append(pd.Series(calculate_errors(truth, injected, v["repairs"],v["columns"], error_func), name=k))
    return df


def save_error(repaired_scenario_dict , path):
    lines = ["solid", "dashed",  "dotted", "dashdot"]
    #colors = ["red", "green", "green",  "green", "purple", "blue"]
    path = f"{path}/error"
    try:
        os.makedirs(path)
    except:
        pass

    scenario_type = repaired_scenario_dict["scenario_type"]
    scenario_data = repaired_scenario_dict["scenario_data"]

    for error in [RMSE,MAE]:
        error_name = error.__name__
        error_path = f'{path}/{error_name}'
        try:
            os.makedirs(error_path)
        except:
            pass

        error_df = generate_error_df(scenario_data, error)
        error_df.index.name = scenario_type.small_data_description


        # plot original error
        columns = list(error_df.columns)
        plt.plot(error_df[columns[0]], marker='o', label=columns[0],
                 ls="dotted", color="red")

        cyclers = {}
        for algo_name in columns[1:]:
            string_representation = error_df.to_string(columns=[algo_name],justify="left")
            with open(f'{error_path}/{algo_name}_{error_name}.txt', "w") as text_file:
                text_file.write(string_representation)
            color = get_alg_color(algo_name)
            if color not in cyclers:
                cyclers[color] = cycle(lines)
            plt.plot(error_df[algo_name],marker='x',label = algo_name ,color=color,ls = next(cyclers[color]))
        plt.xlabel(scenario_type.small_data_description)
        plt.ylabel("error")
        lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(f'{error_path}/{error_name}.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.clf()
        plt.close()

def get_alg_color(function_name):
    for type , color in  ALGORITHM_COLORS.items():
        if type.lower() in function_name.lower():
            return color
    assert False , "function name did not match any algorithm"