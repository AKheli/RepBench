import os

from huber_loss_pca import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale

from Repair.res.Error_Measures import rmse
from Repair.res.file_manipulation import get_df_from_file


def normalized_anomaly_scores(df_original, df_reconstructed):
    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    return minmax_scale(diff)

os.chdir("/".join(__file__.split("/")[:-1]))

df_truth = pd.read_csv("YAHOO.csv")




first_anom = min(df_truth[df_truth["class"] == 1].index[1:])
print(first_anom)

df = pd.read_csv("YAHOO_amplshift.csv").iloc[first_anom-20:first_anom+20,:]
df_truth = df_truth.iloc[first_anom-20:first_anom+20,:]


truth_labels = df["class"]
df = df.drop("class" ,axis=1)

df_train = pd.read_csv("YAHOO_train.csv").iloc[first_anom-20:first_anom+20,:]

print(df_truth)
huber_loss = loss.HuberLoss(delta=1)
train, valid = get_train_valid_sets(df_train, train_size=0.5, random_seed=10)

X_train = train.drop('class', axis=1)
X_test = valid.drop('class', axis=1)

M_rpca = MRobustPCA(3, huber_loss ,  max_iter=10000,eps=1e-11,)

M_rpca.fit(X_train)



#
X_test_reduced = M_rpca.transform(df)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

threshhold = 0.15577889

scores = normalized_anomaly_scores(df,X_test_reconstructed)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

print("false positive" , sum(truth_labels[y_hat_results] == 0) )
print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )
X_test_reconstructed.columns = df.columns

injected = df[df.columns[0]]
truth = df_truth[df.columns[0]]

repair = injected.copy()
repair[y_hat_results] = X_test_reconstructed[df.columns[0]][y_hat_results]


print(rmse(injected,truth))
print(rmse(repair,truth))

M_rpca = MRobustPCA(8, huber_loss ,  max_iter=10000,eps=1e-11,)
M_rpca.fit(df)
X_test_reduced = M_rpca.transform(df)
print(X_test_reduced)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)
threshhold = 0.08577889

scores = normalized_anomaly_scores(df,X_test_reconstructed)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

print("false positive" , sum(truth_labels[y_hat_results] == 0) )
print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )
X_test_reconstructed.columns = df.columns

injected = df[df.columns[0]]
truth = df_truth[df.columns[0]]

repair = injected.copy()
repair[y_hat_results] = X_test_reconstructed[df.columns[0]][y_hat_results]

print(rmse(injected,truth))
print(rmse(repair,truth))
##



#
# # plt.plot(y_hat_results-truth_labels)
# # plt.show()
#
# plt.plot(df["injected"])
# plt.show()
#
# print(X_test_reconstructed)
# X_test_reconstructed.columns = df.columns
#
# plt.plot(X_test_reconstructed["injected"])
# plt.show()
#
# X_test_reconstructed.columns = df.columns
# df_diff = pd.DataFrame({ name : df[name] - X_test_reconstructed[name] for name in df.columns   })
# # plt.plot(df_diff)
# # plt.show()
#
# reconstructed = np.array(X_test_reconstructed["injected"])
# x = np.array(df["injected"])
# repair = x.copy()
# repair[y_hat_results] = reconstructed[y_hat_results]
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
#
#

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