from matplotlib import pyplot as plt

from Injection.Scenarios.scen_gen import build_scenario
from Injection.injected_data_part import InjectedDataContainer
from RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
import matplotlib

from algorithms import CDRecEstimator

matplotlib.use('TKAgg')

import ast

scen_name = "a_size"
anomaly_type = "shift"
data_name = "bafu"
Scenario = build_scenario(scen_name, data_name, a_type=anomaly_type, data_type="train", cols=[0])

# part_scen: InjectedDataContainer
# part_name, part_scen = list(Scenario.part_scenarios.items())[5]
# print(part_name)
#
# cols_to_repair = part_scen.repair_inputs["columns_to_repair"]
#
# plt.rcParams["figure.figsize"] = (8,2)
# plt.plot(part_scen.repair_inputs["injected"].iloc[:, cols_to_repair] , color = "red",label="Anomalous")
# plt.plot(part_scen.repair_inputs["truth"].iloc[:, cols_to_repair] ,color="black",label="Truth")
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/plot.pdf',bbox_inches='tight')
# plt.clf()
# plt.rcParams["figure.figsize"] = (8,1.5)
# for i,delta in enumerate([0.5, 1, 1.2, 2]):
#     rpa = Robust_PCA_estimator(delta=delta)
#     rpa.repair(**part_scen.repair_inputs)
#
#     with open('algorithms/Dimensionality_Reduction/weights.txt', 'r') as f:
#         weights = f.read()
#
#     # with open('algorithms/Dimensionality_Reduction/reduced.txt', 'r') as f:
#     #     reduced = f.read()
#
#         w = ast.literal_eval(weights)
#         # reduced = ast.literal_eval(reduced)
#         #
#         #
#         # # plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/series.svg')
#         # # plt.clf()
#         # #plt.plot(reduced , color = "black")
#         plt.plot(w, label=f"delta={delta}")
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig(f'algorithms/Dimensionality_Reduction/weight_results/delta.pdf',bbox_inches='tight')
# plt.clf()
#
#

rpa = Robust_PCA_estimator(n_max_iter=50)
part_scen: InjectedDataContainer
for part_name, part_scen in Scenario.part_scenarios.items():
    injected_columns = part_scen.repair_inputs["columns_to_repair"]
    truth , injected = part_scen.repair_inputs["truth"].iloc[:,injected_columns] , part_scen.repair_inputs["injected"].iloc[:,injected_columns]
    scores = rpa.scores(**part_scen.repair_inputs)
    repair  = rpa.repair(**part_scen.repair_inputs)

    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


print("------one reduction ------------")
rpa = Robust_PCA_estimator(n_max_iter=0)
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())


print("------CD reduction ------------")
import time
rpa = CDRecEstimator(n_max_iter=20)
start = time.time()
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print(time.time()-start)
print("------one reduction ------------")
rpa = CDRecEstimator(n_max_iter=0)

start = time.time()
for part_name, part_scen in Scenario.part_scenarios.items():
    scores = rpa.scores(**part_scen.repair_inputs)
    print(f"{part_name}&" , round(scores["full_rmse"],3), (truth-injected).abs().sum().sum(),(truth-repair).abs().sum().sum())

print(time.time()-start)
