import pandas as pd
from Repair.algorithms_config import ALGORITHM_COLORS
from Scenarios.metrics import *
from itertools import cycle
import os



def save_error(scenario, path ):
    initial_path = path
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

    full_df = scenario.metrics_df()

    for metric in ["repair_rmse","repair_mae","repair_anomaly_rmse","runtime"]:
        error_name = "_".join(metric.split("_")[1:]) if "_" in metric else metric
        error_path = f'{path}/{error_name}'

        if metric == "runtime":
            error_path =f'{"/".join(initial_path.split("/")[:-2])}/runtime'

        try:
            os.makedirs(error_path)
        except:
            pass

        #save csv files
        df_selection = full_df.applymap(lambda x : (x[metric] , x["name"]))
        print(df_selection)
        for col in df_selection:
            print("col",col)
            new_df = pd.DataFrame(df_selection[col].to_list(), columns=[metric, 'name'])

            new_df.to_csv(f'{error_path}/{col}.txt')

        error_df = full_df.applymap(lambda x : x[metric])
        error_df.to_csv(f'{error_path}/{error_name}.txt')

        # plot original error
        columns = list(error_df.columns)
        # plt.plot(error_df[columns[0]], marker='o', label=columns[0],
        #          ls="dotted", color="red")

        cyclers = {}
        for algo_name in columns:
            color = get_alg_color(algo_name)
            if color not in cyclers:
                cyclers[color] = cycle(lines)
            plt.plot(error_df[algo_name],marker='x',label = algo_name ,color=color,ls = next(cyclers[color]))
        plt.xlabel(error_df.index.name)
        plt.ylabel("error")
        lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(f'{error_path}/{error_name}.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.clf()
        plt.close()

def get_alg_color(function_name):
    print(function_name)
    for type , color in  ALGORITHM_COLORS.items():
        if type.lower() in function_name.lower():
            return color
    return "blue"
    assert False , "function name did not match any algorithm"