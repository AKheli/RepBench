from Repair.repair_algos.Robust_PCA.PCA_algorithms import RPCA1, RPCA2, RPCA3
import pandas as pd
import matplotlib.pyplot as plt

from Scenarios.metrics import RMSE

df_truth = pd.read_csv("Vadetis_test/YAHOO.csv")
df_injected = pd.read_csv("Vadetis_test/YAHOO_amplshift.csv")
df_train = pd.read_csv("Vadetis_test/YAHOO_train.csv")
df_injected = df_injected.drop("class" , axis = 1)

n_components = 2
repair1 = RPCA1(df_injected,df_train , n_components=n_components)
repair2 = RPCA2(df_injected,df_train , n_components=n_components)
repair3 = RPCA3(df_injected,df_train , n_components=n_components , threshold = 0.03)

print("original error", RMSE(df_injected.iloc[:, 0], df_truth.iloc[:, 0]))
print("test and trainset", RMSE(repair1, df_truth.iloc[:, 0]))
print("trainset", RMSE(repair2, df_truth.iloc[:, 0]))
print("refitted on normal df", RMSE(repair3, df_truth.iloc[:, 0]))

injected = df_injected.iloc[:, 0].copy()
for repair , col in zip([repair1,repair2,repair3] , ["blue" , "green" , "yellow"]):
    plt.plot(df_truth.iloc[:,0] , color = "black" )
    plt.plot(df_injected.iloc[:,0] , color = "red")
    plt.plot(repair , color = col)
plt.show()

# # changes = np.array(injected != repair1 , dtype=bool)
# # plt.plot(np.arange(len(changes))[changes], injected[changes],color = "red")
# # plt.plot(np.arange(len(changes))[changes], repair1[changes])
# # plt.show()
