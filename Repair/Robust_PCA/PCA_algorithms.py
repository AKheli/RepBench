import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale

from Repair.Algorithms_Config import ALGORITHM_PARAMETERS, RPCA
from Repair.Robust_PCA import loss
from Repair.Robust_PCA.helpers import normalized_anomaly_scores
from Repair.Robust_PCA.huber_loss_pca import get_train_valid_sets
from Repair.Robust_PCA.m_est_rpca import MRobustPCA
from Repair.res.timer import Timer
from Scenarios.metrics import rmse
import matplotlib.pyplot as plt

os.chdir("/".join(__file__.split("/")[:-1]))


def normalized_scores(x, y):
    diff = (x - y) ** 2
    diff = pd.Series(data=diff)
    return minmax_scale(diff)


huber_loss = loss.HuberLoss(delta=1)


def check_valid_input(injected, train):
    assert "class" in train.columns, "class in train columns"


def get_threshhold(fitted_M_rcpa, test, test_class):
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


def reconstuct(injected, M_rpca):
    Repair_reduced = M_rpca.transform(injected)
    Repair_reduced = pd.DataFrame(data=Repair_reduced)
    Repair_reconstructed = M_rpca.inverse_transform(Repair_reduced)
    Repair_reconstructed = pd.DataFrame(data=Repair_reconstructed)

    # print(np.array(injected))
    # print(np.array(Repair_reconstructed))

    return Repair_reconstructed


def repair_result_df(injected, to_repair_cols, reconstructed_cols, repair_booleans, col):
    to_repair_cols[repair_booleans] = reconstructed_cols[repair_booleans]
    result = injected.copy()
    result.iloc[:, col] = to_repair_cols
    return result

alg_type = RPCA
default_params = ALGORITHM_PARAMETERS[alg_type]
def RPCA1(injected, train, train_class, n_components=2, cols=0, threshold=None, **kwargs):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    train["class"] = train_class
    train, valid = get_train_valid_sets(train, train_size=0.5, random_seed=100)

    X_train = train.drop('class', axis=1)
    test_class = valid["class"]
    X_test = valid.drop('class', axis=1)

    timer = Timer()
    timer.start()

    M_rpca = MRobustPCA(n_components, huber_loss)

    # Fit R-PCA on Train Set
    M_rpca.fit(X_train)

    if threshold is None:
        threshold = get_threshhold(M_rpca, X_test, test_class)

    Repair_reconstructed = reconstuct(injected, M_rpca)
    result = injected.copy()

    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        y_repair_scores = normalized_scores(to_repair_cols, reconstructed_cols)
        to_repair_booleans = y_repair_scores > threshold

        # replace value in original df
        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed , "runtime": timer.get_time() ,"type" : alg_type}



def add_shift(df, p):
    original_cols = list(df.columns)
    to_concat = []
    for i in range(p):
        right = df.shift(periods=i, fill_value=0)
        right.columns = [f"{c}_{i}" for c in original_cols]
        left = df.shift(periods=-i, fill_value=0)
        left.columns = [f"{c}_{-i}" for c in original_cols]
        to_concat.append(right)
        to_concat.append(left)

    return pd.concat([df] + to_concat, axis=1)


def RPCA2(injected,cols, n_components=1,  threshold=1, return_reconstructed=False, **kwargs):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass
    timer = Timer()
    timer.start()

    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
    M_rpca.fit(injected)


    Repair_reconstructed = reconstuct(injected, M_rpca)

    result = injected.copy()
    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff*0 if std == 0 else abs((diff - mean) / std)
        if std == 0:
            print("RPCA2 no repair")
        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    # Repair_reconstructed.plot()
    # result.plot()
    # plt.title("pca")
    # plt.show()

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed , "runtime": timer.get_time() ,"type" : alg_type}

def RPCA3(injected,cols, n_components=2, threshold=2.2, return_reconstructed=False, **kwargs):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass
    timer = Timer()
    timer.start()

    #injected = add_shift(injected,0)
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.01))
    np.random.seed(100)
    sampled = injected.sample(n=1000,axis='rows',replace=True)
    M_rpca.fit(sampled )
    print(M_rpca.components_)

    Repair_reconstructed = reconstuct(injected, M_rpca)

    result = injected.copy()
    for col in cols:
        reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
        to_repair_cols = np.array(injected.iloc[:, col])

        diff = reconstructed_cols - to_repair_cols

        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff*0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
        result.iloc[:, col] = to_repair_cols

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed , "runtime": timer.get_time() ,"type" : alg_type}

def RPCA_no_train_2(injected, truth=None, n_components=2, col=0, threshold=1.5, return_reconstructed=False, **kwargs):
    """
       uses the whole train to calculate threshold and refits on normal set
       """

    dif = (injected.max() - injected.min())
    min_ = injected.min()
    injected = (injected - min_) / dif
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    p = 5
    original_cols = list(injected.columns)

    to_concat = []
    for i in range(p):
        right = injected.shift(periods=i, fill_value=0)
        right.columns = [f"{c}_{i}" for c in original_cols]
        left = injected.shift(periods=-i, fill_value=0)
        left.columns = [f"{c}_{-i}" for c in original_cols]
        to_concat.append(right)
        to_concat.append(left)

    injected = pd.concat([injected] + to_concat, axis=1)
    M_rpca = MRobustPCA(n_components, loss.HuberLoss(delta=0.001), model="first")
    M_rpca.fit(injected)


    Repair_reconstructed = reconstuct(injected, M_rpca)
    reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
    to_repair_cols = np.array(injected.iloc[:, col])

    diff = reconstructed_cols - to_repair_cols
    m = np.mean(diff)
    std = np.std(diff)
    abs_z_score = abs((diff - m) / std)

    to_repair_booleans = abs_z_score > threshold

    to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
    result = injected.copy()
    result.iloc[:, col] = to_repair_cols
    result = result[original_cols]


    x= np.array(injected)
    # plt.title("injected")
    # plt.plot(x)
    # plt.plot(M_rpca.weights_)
    # plt.show()

    #
    # truth.iloc[:, col].plot()
    # plt.title("truth")
    #
    # Repair_reconstructed.iloc[:, col].plot()
    # plt.title("reconstructed")
    # plt.show()
    #
    # result.iloc[:, col].plot()
    # plt.title("result")
    # plt.show()

    # injected.plot()
    # Repair_reconstructed.plot()
    # result.plot()
    # plt.title("pca")
    # plt.show()
    result = result * dif + min_
    return {"repair": result, "PCA_reconstructed": Repair_reconstructed }


import sklearn.decomposition


def PCA_leave_out(injected, col=0, threshold=1, return_reconstructed=False, **kwargs):
    """
    uses the whole train to calculate threshold and refits on normal set
    """
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    pca = sklearn.decomposition.PCA(n_components=2)
    X_train_PCA = pca.fit_transform(injected)
    pca.components_[0, :] = 0  # pca.components_[2,:]*0.5
    X_train_PCA = pd.DataFrame(data=X_train_PCA, index=injected.index)
    X_train_PCA_inverse = pca.inverse_transform(X_train_PCA)
    Repair_reconstructed = pd.DataFrame(data=X_train_PCA_inverse, index=injected.index)

    if return_reconstructed:
        return Repair_reconstructed

    reconstructed_cols = np.array(Repair_reconstructed.iloc[:, col])
    to_repair_cols = np.array(injected.iloc[:, col])

    diff = reconstructed_cols - to_repair_cols

    mean = np.mean(diff)
    std = np.std(diff)
    abs_z_score = abs((diff - mean) / std)
    to_repair_booleans = abs_z_score > threshold

    to_repair_cols[to_repair_booleans] = reconstructed_cols[to_repair_booleans]
    result = injected.copy()
    result.iloc[:, col] = to_repair_cols
    print("injected_rank", np.linalg.matrix_rank(np.array(injected)))
    print("COMPONENTS", pca.components_)
    print(np.linalg.matrix_rank(np.dot(np.array(X_train_PCA), pca.components_)))
    print(np.linalg.matrix_rank(np.dot(np.array(X_train_PCA), pca.components_) + pca.mean_))

    return {"repair": result, "PCA_reconstructed": Repair_reconstructed}
