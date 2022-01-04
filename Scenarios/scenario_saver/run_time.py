import os
from itertools import cycle

import pandas as pd
from matplotlib import pyplot as plt


def scenario_part_runtime(repairs):
    runtimes = {}
    for algo_name, algo_output in repairs.items():
        runtimes[algo_name] = algo_output["runtime"]
    return runtimes


def generate_runtime_df(values):
    df = pd.DataFrame()
    for k, v in values.items():
        df = df.append(pd.Series(scenario_part_runtime(v["repairs"]), name=k))
    return df

def save_runtime(repaired_scenario_dict , path):
    lines = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
    linecycler = cycle(lines)

    path = f"{path}/runtime"
    try:
        os.makedirs(path)
    except:
        pass

    scenario_data = repaired_scenario_dict["scenario_data"]
    scenario_type = repaired_scenario_dict["scenario_type"]
    runtime_df = generate_runtime_df(scenario_data)
    runtime_df.index.name = scenario_type.small_data_description

    for algo in list(runtime_df.columns):
        string_representation = runtime_df.to_string(columns=[algo], justify="left")

        with open(f'{path}/{algo}_runtime.txt', "w") as text_file:
            text_file.write(string_representation)
    for col in runtime_df.columns:
        plt.plot(runtime_df[col], marker='x', label=col, ls=next(linecycler))
    plt.xlabel(scenario_type.small_data_description)
    plt.ylabel("runtime")
    plt.legend()
    plt.savefig(f'{path}/runtime.png')
    plt.clf()
    plt.close()