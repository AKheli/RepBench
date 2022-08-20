### run from top level directory
from repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator
from repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Scenarios.scenario import Scenario
from Scenarios.data_part import DataPart
import matplotlib.pyplot as plt
import pandas as pd

scen = Scenario("base","humidity.csv","shift")

_ , scenario_part= list(scen.part_scenarios.items())[0]

scenario_part : DataPart = scenario_part

injected = scenario_part.train.repair_inputs["injected"]
truth    =   scenario_part.train.repair_inputs["truth"]

cut = lambda df , label : plt.plot(df.iloc[650:, [0]].values,label = label)



for k in [2,3,4]:
    cut(truth, "truth")
    cut(injected, "anomalous")
    pca_estim = Robust_PCA_estimator(classification_truncation=k,repair_truncation=3,n_max_iter=0)
    pca_estim.repair(injected=injected,truth = None ,columns_to_repair=scenario_part.injected_columns)
    print(pca_estim.weighted_mean[0])

    cut(pd.DataFrame(pca_estim.reduced),"pca")


    pca_estim = Robust_PCA_estimator(classification_truncation=k,repair_truncation=3,n_max_iter=10)
    pca_estim.repair(injected=injected,truth = None ,columns_to_repair=scenario_part.injected_columns)
    print(pca_estim.weighted_mean[0])

    cut(pd.DataFrame(pca_estim.reduced),"rpca")

    pca_estim = Robust_PCA_estimator(classification_truncation=k,repair_truncation=3,n_max_iter=100)
    pca_estim.repair(injected=injected,truth = None ,columns_to_repair=scenario_part.injected_columns)
    print(pca_estim.weighted_mean[0])

    cut(pd.DataFrame(pca_estim.reduced),"rpca100")

    pca_estim = CDRecEstimator(classification_truncation=k,repair_truncation=3,n_max_iter=0)
    pca_estim.repair(injected=injected,truth = None ,columns_to_repair=scenario_part.injected_columns)
    print(pca_estim.weighted_mean[0])

    cut(pd.DataFrame(pca_estim.reduced),"cd0")

    pca_estim = CDRecEstimator(classification_truncation=k,repair_truncation=3,n_max_iter=10)
    pca_estim.repair(injected=injected,truth = None ,columns_to_repair=scenario_part.injected_columns)
    print(pca_estim.weighted_mean[0])

    cut(pd.DataFrame(pca_estim.reduced),"cd10")


    plt.legend()
    plt.title(k)
    plt.show()