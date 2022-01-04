from Repair.Robust_PCA.PCA_algorithms import *
from Repair.Robust_PCA.huber_loss_pca import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale


def normalized_anomaly_scores(df_original, df_reconstructed):
    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    return minmax_scale(diff)

os.chdir("/".join(__file__.split("/")[:-1]))

injected_file = "humidity_amp.csv"
train_file = "humidity_train.csv"


df = pd.read_csv(injected_file)
truth_labels = df["class"].iloc[:200]
df = df.drop("class" ,axis=1)
df = df.iloc[:200,:4]

df_train = pd.read_csv(train_file).iloc[400:600,[1,2,3,4,-1]]

huber_loss = loss.HuberLoss(delta=1)
train, valid = get_train_valid_sets(df_train, train_size=0.5, random_seed=10)

X_train = train.drop('class', axis=1)
X_test = valid.drop('class', axis=1)

M_rpca = MRobustPCA(2, huber_loss)

M_rpca.fit(X_train)
#
X_test_reduced = M_rpca.transform(df)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

threshhold = 0.0854271

scores = normalized_anomaly_scores(df,X_test_reconstructed)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

print("false positive" , sum(truth_labels[y_hat_results] == 0) )
print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )


repair = RPCA4(df,None , n_components = 1 ,return_reconstructed=True)

plt.plot(df)
plt.show()
plt.plot(repair)
plt.show()

scores = normalized_anomaly_scores(df,repair)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

print("false positive RPCA4" , sum(truth_labels[y_hat_results] == 0) )
print("false negative RPCA4" , sum(truth_labels[y_hat_results==0] == 1) )


repair = RPCA1(df,df_train, n_components = 2 ,return_reconstructed=True)
scores = normalized_anomaly_scores(df,repair)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)

print("false positive" , sum(truth_labels[y_hat_results] == 0) )
print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )

plt.plot(repair)
plt.show()
plt.plot(X_train)
plt.show()



repair = PCA(df,df_train, n_components = 4 ,return_reconstructed=True)
scores = normalized_anomaly_scores(df,repair)
scores = np.round(scores, 7)
y_hat_results = (scores > threshhold).astype(bool)
print("PCA")
print("false positive" , sum(truth_labels[y_hat_results] == 0) )
print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )

plt.plot(repair)
plt.show()

#
# X_test_reconstructed.columns = df.columns
#
# injected = df[df.columns[0]]
# truth = df_truth[df.columns[0]]
#
# repair = injected.copy()
# repair[y_hat_results] = X_test_reconstructed[df.columns[0]][y_hat_results]
#
#
# print(RMSE(injected, truth))
# print(RMSE(repair, truth))
#
# M_rpca = MRobustPCA(2, huber_loss ,  max_iter=10000,eps=1e-11,)
# M_rpca.fit(df)
# X_test_reduced = M_rpca.transform(df)
# print(X_test_reduced)
# X_test_reduced = pd.DataFrame(data=X_test_reduced)
# X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
# X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)
# threshhold = 0.08577889
#
# scores = normalized_anomaly_scores(df,X_test_reconstructed)
# scores = np.round(scores, 7)
# y_hat_results = (scores > threshhold).astype(bool)
#
# print("false positive" , sum(truth_labels[y_hat_results] == 0) )
# print("false negative" , sum(truth_labels[y_hat_results==0] == 1) )
# X_test_reconstructed.columns = df.columns
#
# injected = df[df.columns[0]]
# truth = df_truth[df.columns[0]]
#
# repair = injected.copy()
# repair[y_hat_results] = X_test_reconstructed[df.columns[0]][y_hat_results]
#
# print(RMSE(injected, truth))
# print(RMSE(repair, truth))
# ##
#


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