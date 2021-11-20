import sys
import os

sys.path.append('../../../')

from Repair.res.Measures import *
from huber_loss_pca import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale

from Repair.res.file_manipulation import get_df_from_file

os.chdir("/".join(os.getcwd().split("/")[:-2]))


def normalized_anomaly_scores(df_original, df_reconstructed):
    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    return minmax_scale(diff)


df = get_df_from_file("Data/Injected_data/multiple_series/3_amp_shiftsYAHOO.csv")
print(df)
truth_labels = df["class"]
truth = df["truth"]
df = df.drop("class" ,axis=1)
df = df.drop("index" ,axis=1)
df = df.drop("truth" ,axis=1)


huber_loss = loss.HuberLoss(delta=1)

M_rpca = MRobustPCA(2, huber_loss)

M_rpca.fit(df)
X_test_reduced = M_rpca.transform(df)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

threshhold = 0.1

scores = normalized_anomaly_scores(df,X_test_reconstructed)
scores = np.round(scores, 7)
y_hat_results = (scores >threshhold).astype(bool)


# plt.plot(y_hat_results-truth_labels)
# plt.show()

# plt.show()



X_test_reconstructed.columns = df.columns
df_diff = pd.DataFrame({ name : df[name] - X_test_reconstructed[name] for name in df.columns   })
# plt.plot(df_diff)
# plt.show()

d = np.array(df_diff["injected"])
y_hat_results = abs(np.median(d))*2 > abs(d)

x = np.array(df["injected"].copy() )

y = np.array(X_test_reconstructed["injected"])
#print(y_hat_results)
print(x[y_hat_results])
x[y_hat_results] = y[y_hat_results]
print(x[y_hat_results])

plt.plot(truth , label = "truth")
plt.plot(np.array(df["injected"] ) , label = "injected")
plt.plot(y ,label =  "reconstructed")
plt.plot(x ,label =  "repair")
plt.legend()
plt.show()

print(rmse(truth,X_test_reconstructed["injected"]))
print(rmse(truth,x))
print(rmse(truth,truth))

plt.plot(df["injected"]-truth)
plt.plot(y-truth)

#plt.plot(x-truth)

plt.show()
# plt.plot(y_hat_results)
# plt.show()
#
# print("original" , rmse(truth,np.array(df["injected"])))
# x = np.array(df["injected"])
# y_hat_results = np.array(truth_labels,dtype=bool)
# x[y_hat_results] = y[y_hat_results]
# print("class changed", rmse(truth, x))
#
# print()
# for i in [1,2,3,4,5,10,100,1000,10000,1000000,10000000]:
#     x = np.array(df["injected"])
#     y_hat_results = (abs(np.median(d))*i) < abs(d)
#     x[y_hat_results] = y[y_hat_results]
#     print(i,rmse(truth,x))
#
#
# screen_result = SCREEN_repair(np.array(df["injected"]),smax=100,smin=-100)["repair"]
# print(screen_result)
# print("screen" ,  rmse(truth, screen_result))

plt.close()
plt.plot(df["injected"])
plt.show()