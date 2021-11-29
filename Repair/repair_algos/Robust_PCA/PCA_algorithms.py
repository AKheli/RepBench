import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale

from Repair.repair_algos.Robust_PCA import loss
from Repair.repair_algos.Robust_PCA.helpers import normalized_anomaly_scores
from Repair.repair_algos.Robust_PCA.huber_loss_pca import get_train_valid_sets
from Repair.repair_algos.Robust_PCA.m_est_rpca import MRobustPCA
from Repair.res.Error_Measures import rmse
import matplotlib.pyplot as plt
os.chdir("/".join(__file__.split("/")[:-1]))

def normalized_scores(x,y):
    diff = (x-y) ** 2
    diff = pd.Series(data=diff)
    return minmax_scale(diff)


huber_loss = loss.HuberLoss(delta=5)
def check_valid_input(injected, train):
    assert "class" in train.columns , "class in train columns"

def get_threshhold(fitted_M_rcpa,test , test_class):
    # R-PCA on Test Set
    X_test_reduced = fitted_M_rcpa.transform(test)
    X_test_reduced = pd.DataFrame(data=X_test_reduced, index=test.index)
    X_test_reconstructed = fitted_M_rcpa.inverse_transform(X_test_reduced)
    X_test_reconstructed = pd.DataFrame(data=X_test_reconstructed, index=test.index)

    y_test_scores = normalized_anomaly_scores(test, X_test_reconstructed, axis=1)
    y_test_scores = np.round(y_test_scores, 7)  # round scores

    # computed scores are always in between 0-1 due to min max normalization
    thresholds = np.linspace(0, 1, 200)
    thresholds = np.round(thresholds, 7)  # round thresholds
    old_res = (np.inf, 0)
    for i in thresholds:
        class_prediction = np.zeros(len(test_class))
        class_prediction[y_test_scores > i] = 1
        res = rmse(class_prediction, test_class)
        if res < old_res[0]:
            old_res = (res, i)
    threshold = old_res[1]
    return threshold


def RPCA1(injected, train_set , n_components = 2,  col = 0  ):
    try:
        injected = injected.drop("class" , axis = 1)
    except:
        pass

    train, valid = get_train_valid_sets(train_set, train_size=0.5, random_seed=10)
    X_train = train.drop('class', axis=1)
    test_class = valid["class"]
    X_test = valid.drop('class', axis=1)

    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    threshold = get_threshhold(M_rpca, X_test , test_class)

    #print("threshhold" , threshold)
    repair = np.array(injected.iloc[:,col])
    Repair_reduced = M_rpca.transform(injected)
    Repair_reduced = pd.DataFrame(data=Repair_reduced)
    Repair_reconstructed = M_rpca.inverse_transform(Repair_reduced)
    Repair_reconstructed = np.array(pd.DataFrame(data=Repair_reconstructed).iloc[:,col])

    y_repair_scores = normalized_scores(repair, Repair_reconstructed)
    repair[y_repair_scores > threshold] = Repair_reconstructed[y_repair_scores > threshold]
    """
    uses the fit from the train set
    """
    return repair



def RPCA2(injected, train_set ,n_components = 2, col = 0 , threshold = None):
    """
    uses the whole train to fit
    """
    try:
        injected = injected.drop("class" , axis = 1)
    except:
        pass
    train_class = train_set["class"]
    X_train = train_set.drop('class', axis=1)
    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    if threshold is None:
        threshold = get_threshhold(M_rpca, X_train, train_class)

    #print("threshhold", threshold)
    repair = np.array(injected.iloc[:, col])
    Repair_reduced = M_rpca.transform(injected)
    Repair_reduced = pd.DataFrame(data=Repair_reduced)
    Repair_reconstructed = M_rpca.inverse_transform(Repair_reduced)
    Repair_reconstructed = np.array(pd.DataFrame(data=Repair_reconstructed).iloc[:, col])

    y_repair_scores = normalized_scores(repair, Repair_reconstructed)

    repair[y_repair_scores > threshold] = Repair_reconstructed[y_repair_scores > threshold]
    return repair

def RPCA3(injected, train_set ,n_components = 2, col = 0 , threshold = None):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    try:
        injected = injected.drop("class" , axis = 1)
    except:
        pass

    train_class = train_set["class"]
    X_train = train_set.drop('class', axis=1)
    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    if threshold is None:
        threshold = get_threshhold(M_rpca, X_train, train_class)

    #print("threshhold", threshold)
    try:
        injected.drop("class" , axis = 1)
    except:
        pass
    M_rpca = MRobustPCA(n_components, huber_loss)
    M_rpca.fit(injected)
    repair = np.array(injected.iloc[:, col])
    Repair_reduced = M_rpca.transform(injected)
    Repair_reduced = pd.DataFrame(data=Repair_reduced)
    Repair_reconstructed = M_rpca.inverse_transform(Repair_reduced)
    Repair_reconstructed = np.array(pd.DataFrame(data=Repair_reconstructed).iloc[:, col])

    y_repair_scores = normalized_scores(repair, Repair_reconstructed)

    repair[y_repair_scores > threshold] = Repair_reconstructed[y_repair_scores > threshold]
    return repair


def RPCA4(injected, train_set ,n_components = 2, col = 0 , threshold = None):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    injected_class = np.array(injected["class" ],dtype=bool)
    try:
        injected = injected.drop("class" , axis = 1)
    except:
        pass
    M_rpca = MRobustPCA(n_components, huber_loss)
    M_rpca.fit(injected)
    repair = np.array(injected.iloc[:, col])
    Repair_reduced = M_rpca.transform(injected)
    Repair_reduced = pd.DataFrame(data=Repair_reduced)
    Repair_reconstructed = M_rpca.inverse_transform(Repair_reduced)
    Repair_reconstructed = np.array(pd.DataFrame(data=Repair_reconstructed).iloc[:, col])

    diff = repair - Repair_reconstructed
    mean =  np.mean(diff)
    std = np.std(diff)
    z_score = (diff-mean)/std
    # print(z_score)
    # print(sorted(z_score))
    # plt.plot(abs(z_score))
    # plt.plot(repair)
    # plt.plot(Repair_reconstructed)

    treshhold = 2
    to_repair = abs(z_score)  >treshhold
    print("repair but not class" ,sum(to_repair > injected_class))
    print("class but not repaired",sum(to_repair < injected_class))

    repair[abs(z_score)  >treshhold] = Repair_reconstructed[abs(z_score)  > treshhold]
    # plt.plot(repair)
    # plt.show()

    return repair


import sklearn.decomposition
def PCA(injected, train_set ,n_components = 2, col = 0 , threshold = None):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    try:
        injected = injected.drop("class" , axis = 1)
    except:
        pass

    whiten = False
    random_state = 2018
    pca = sklearn.decomposition.PCA(n_components=n_components)
    X_train_PCA = pca.fit_transform(injected)
    X_train_PCA = pd.DataFrame(data=X_train_PCA, index=injected.index)
    X_train_PCA_inverse = pca.inverse_transform(X_train_PCA)
    Repair_reconstructed = np.array(pd.DataFrame(data=X_train_PCA_inverse, \
                                      index=injected.index).iloc[:,col])
    repair = np.array(injected.iloc[:, col])
    diff = repair - Repair_reconstructed
    mean =  np.mean(diff)
    std = np.std(diff)
    z_score = (diff-mean)/std
    # print(z_score)
    # print(sorted(z_score))
    # plt.plot(abs(z_score))
    # plt.plot(repair)
    # plt.plot(Repair_reconstructed)
    # plt.show()
    treshhold = 3
    repair[abs(z_score)  >treshhold] = Repair_reconstructed[abs(z_score)  > treshhold]
    return repair


