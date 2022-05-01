import numpy as np
import pandas as pd
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Repair.algorithms_config import ALGORITHM_COLORS
from Scenarios.metrics import *
from itertools import cycle
import os

from Scenarios.senario_methods import generate_error_df_and_error_tables

errors = [RMSE,MAE]

def latex_str(path , error_df , error_name):
    r = ""
    r+=f"xlabel = _{error_df.index.name}-\n"
    r+=f"ylabel=_{error_name}-\n"
    x_ticks = f"xtick=_"
    for i in error_df.index:
        x_ticks += f"{i},"
    x_ticks = x_ticks[:-1]+"-\n"
    r+=x_ticks
    y_ticks = f"ytick=_"
    for x in np.arange(0, error_df.max().max(), step=0.2):
        y_ticks += f"{round(x,1)},"
    y_ticks = y_ticks[:-1] + "-\n"
    r += y_ticks
    legend = "\legend_"
    for column in error_df.columns:
        legend += f"{column},"
        coordinates = ""
        for i,c in zip(error_df.index,error_df[column]):
            coordinates += f"({i,c})"

        r+= f"\\addplot \n coordinates_{coordinates}-; \n"
    legend = legend[:-1]+"-"
    r+=legend
    r= r.replace("_","{")
    r = r.replace("-","}")
    r = r.replace("((", "(")
    r = r.replace("))", ")")

    print(r)
    with open(f'{path}/{error_name}_for_text.txt', "w") as text_file:
        text_file.write(r)

    pass

def save_error(repaired_scenario : BaseScenario, path ):
    lines = ["solid", "dashed",  "dotted", "dashdot"]
    #colors = ["red", "green", "green",  "green", "purple", "blue"]
    path = f"{path}/error"
    try:
        os.makedirs(path)
    except:
        pass

    ## todo check why there was a plot here before
    plt.clf()
    plt.close()

    for error in errors:
        error_name = error.__name__
        error_path = f'{path}/{error_name}'
        try:
            os.makedirs(error_path)
        except:
            pass

        error_df , error_tables  = generate_error_df_and_error_tables(repaired_scenario, error)
        error_df.index.name = repaired_scenario.small_data_description

        #save csv files
        for alg_error , values in error_tables.items():
            values.to_csv(f'{error_path}/{alg_error}.txt')

        error_df.to_csv(f'{error_path}/{error_name}.txt')
        latex_str(error_path,error_df,error_name)

        # plot original error
        columns = list(error_df.columns)
        plt.plot(error_df[columns[0]], marker='o', label=columns[0],
                 ls="dotted", color="red")

        cyclers = {}
        for algo_name in columns[1:]:
            # string_representation = error_df.to_string(columns=[algo_name],justify="left")
            # with open(f'{error_path}/{algo_name}_{error_name}.txt', "w") as text_file:
            #     text_file.write(string_representation)
            color = get_alg_color(algo_name)
            if color not in cyclers:
                cyclers[color] = cycle(lines)
            plt.plot(error_df[algo_name],marker='x',label = algo_name ,color=color,ls = next(cyclers[color]))
        plt.xlabel(repaired_scenario.small_data_description)
        plt.ylabel("error")
        lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(f'{error_path}/{error_name}.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.clf()
        plt.close()

def get_alg_color(function_name):
    for type , color in  ALGORITHM_COLORS.items():
        if type.lower() in function_name.lower():
            return color
    return "blue"
    assert False , "function name did not match any algorithm"