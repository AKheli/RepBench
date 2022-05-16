# import os
# from itertools import cycle
#
# import pandas as pd
# from matplotlib import pyplot as plt
#
#
#
# def scenario_part_runtime(repairs):
#     runtimes = {}
#     for algo_name, algo_output in repairs.items():
#         runtimes[algo_name] = algo_output["runtime"]
#     return runtimes
#
#
# def generate_runtime_df(repairs):
#     df = pd.DataFrame()
#     for scen, repairs_ in repairs.items():
#         df = df.append(pd.Series(scenario_part_runtime(repairs_), name=scen))
#     return df
#
# def save_runtime(repaired_scenario :BaseScenario, path):
#     pass
#     # lines = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
#     # linecycler = cycle(lines)
#     #
#     # path = f"{path}/runtime"
#     # try:
#     #     os.makedirs(path)
#     # except:
#     #     pass
#     #
#     #
#     # scenario_repair = repaired_scenario.repairs
#     # scenario_type = repaired_scenario.scenario_type
#     # runtime_df = generate_runtime_df(scenario_repair)
#     # runtime_df.index.name = repaired_scenario.small_data_description
#     #
#     # runtime_df.to_csv(f'{path}/runtime.txt')
#     #
#     # for algo in list(runtime_df.columns):
#     #     string_representation = runtime_df.to_string(columns=[algo], justify="left")
#     #
#     #     with open(f'{path}/{algo}_runtime.txt', "w") as text_file:
#     #         text_file.write(string_representation)
#     # for col in runtime_df.columns:
#     #     plt.plot(runtime_df[col], marker='x', label=col, ls=next(linecycler))
#     # plt.xlabel(repaired_scenario.small_data_description)
#     # plt.ylabel("runtime")
#     # plt.legend()
#     # plt.savefig(f'{path}/runtime.png')
#     # plt.clf()
#     # plt.close()