
from huber_loss_pca import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale

from Scenarios.metrics import RMSE
from Repair.res.file_manipulation import get_df_from_file


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


df_train = get_df_from_file("Data/train/YAHOOtrain.csv", is_train=True)
huber_loss = loss.HuberLoss(delta=1)

df_train = df_train.iloc[range(5),:]
X_train = df_train.drop('class', axis=1)


M_rpca = MRobustPCA(3, huber_loss)

M_rpca.fit(X_train)



X_test_reduced = M_rpca.transform(df)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

threshhold = 0.09959799

scores = normalized_anomaly_scores(df,X_test_reconstructed)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

# plt.plot(y_hat_results-truth_labels)
# plt.show()

plt.plot(df["injected"])
plt.show()

print(X_test_reconstructed)
X_test_reconstructed.columns = df.columns

plt.plot(X_test_reconstructed["injected"])
plt.show()

X_test_reconstructed.columns = df.columns
df_diff = pd.DataFrame({ name : df[name] - X_test_reconstructed[name] for name in df.columns   })
# plt.plot(df_diff)
# plt.show()

reconstructed = np.array(X_test_reconstructed["injected"])
x = np.array(df["injected"])
repair = x.copy()
repair[y_hat_results] = reconstructed[y_hat_results]

plt.plot(x,lw = 1, label = "anomaly",color="red")
plt.plot(truth,lw = 2, label = "truth" , color = "black")
plt.plot(repair,lw = 1, label = "repair")
plt.legend()
plt.show()

print(sum(y_hat_results))
print( "original", RMSE(truth, x))
print("pca reconstructed", RMSE(truth, reconstructed))
print("repair", RMSE(truth, repair))



## run again
# print(X_test_reconstructed)
# X_test_reduced = M_rpca.transform(X_test_reconstructed)
# X_test_reduced = pd.DataFrame(data=X_test_reduced)
# X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
# X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)
#
# threshhold = 0.09959799
#
# scores = normalized_anomaly_scores(df,X_test_reconstructed)
# scores = np.round(scores, 7)
# y_hat_results = (scores > threshhold).astype(bool)
#
# X_test_reconstructed.columns = df.columns
# reconstructed = np.array(X_test_reconstructed["injected"])
# x = np.array(df["injected"])
# repair = x.copy()
# repair[y_hat_results] = reconstructed[y_hat_results]
#
#
# plt.plot(x,lw = 1, label = "anomaly",color="red")
# plt.plot(truth,lw = 2, label = "truth" , color = "black")
# plt.plot(repair,lw = 1, label = "repair")
# plt.legend()
# plt.show()
#
# print(sum(y_hat_results))
# print( "original" , rmse(truth,x) )
# print("pca reconstructed" ,  rmse(truth,reconstructed))
# print("repair" , rmse(truth,repair))

