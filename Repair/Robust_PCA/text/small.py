import os

import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from Repair.Robust_PCA.huber_loss_pca import *


def normalized_anomaly_scores(df_original, df_reconstructed):
    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=1)
    diff = pd.Series(data=diff, index=df_original.index)
    return minmax_scale(diff)

os.chdir("/".join(__file__.split("/")[:-1]))

os.listdir()
df_truth = pd.read_csv("YAHOO_original").iloc[200:550,:8]
df_injected = pd.read_csv("YAHOO_injected").iloc[200:550,:8]
df_train = pd.read_csv("YAHOO_injected").iloc[:100,:8]
df_train_truth = pd.read_csv("YAHOO_original").iloc[:100,:8]


plt.plot(df_truth.iloc[:,0])
plt.plot(df_injected.iloc[:,0])
plt.plot(df_train.iloc[:,0])
plt.plot(df_train_truth.iloc[:,0])
plt.show()

print(df_truth)

#df_train["class"] = df_train_truth.iloc[:,0] == df_train.iloc[:,0]
huber_loss = loss.HuberLoss(delta=10)
# train, valid = get_train_valid_sets(df_train, train_size=0.6, random_seed=10)
#
# X_train = train.drop('class', axis=1)
# X_test = valid.drop('class', axis=1)

M_rpca = MRobustPCA(2, huber_loss ,  max_iter=1000,eps=1e-9,)

M_rpca.fit(df_train)
X_test_reduced = M_rpca.transform(df_train)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

X_test_reconstructed.columns = df_train.columns
plt.plot(X_test_reconstructed.iloc[:,0])
plt.plot(df_train.iloc[:,0])

plt.show()

M_rpca = MRobustPCA(2, huber_loss ,  max_iter=1000,eps=1e-9,)
M_rpca.fit(df_train)

X_test_reduced = M_rpca.transform(df_injected)
X_test_reduced = pd.DataFrame(data=X_test_reduced)
X_test_reconstructed = M_rpca.inverse_transform(X_test_reduced)
X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed)

X_test_reconstructed.columns = df_injected.columns
X_test_reconstructed.index = df_injected.index

plt.plot(X_test_reconstructed.iloc[:,0] , label = "reconstrcuted" , alpha=0.5)
plt.plot(df_injected.iloc[:,0] , label = "injected",alpha=0.5)
#plt.legend()
plt.show()
