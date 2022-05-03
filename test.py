from Repair.repair_algorithm import RepairAlgorithm
from Scenarios.scenario_types.AnomalyRate import AnomalyRateScenario

import matplotlib.pyplot as plt

cols = [0]

repair_alg = RepairAlgorithm("cdrec", cols)
anomaly = "shift"
data = "msd.csv"
injected_scenario = AnomalyRateScenario(data, cols, anomaly_type=
anomaly)

repair_alg.estimator.refit = True
for (name, train, test) in injected_scenario.name_train_test_iter:
    train["injected"].iloc[:, cols].plot()
    plt.show()

    repair_alg.train(**train)
    print("trained")
    repair_train = repair_alg.repair(**train)["repair"]
    print("repaired train")
    repair_train.iloc[:, cols].plot()
    plt.show()
    break

for (name, train, test) in injected_scenario.name_train_test_iter:
    print("repaired test")
    repair_test = repair_alg.repair(**test)["repair"]
    repair_test.iloc[:, cols].plot()
    plt.show()
