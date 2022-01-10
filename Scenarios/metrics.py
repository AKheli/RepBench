import numpy as np
import scipy
import sklearn.metrics as sm
import matplotlib.pyplot as plt


def process(df_1, df_2, cols, labels=None):
    l = [] if labels is None else labels
    x_res = []
    y_res = []
    for i in cols:
        x = np.array(df_1.iloc[:, i])
        y = np.array(df_2.iloc[:, i])
        x[l] = 0.0
        y[l] = 0.0
        x_res.append(x)
        y_res.append(y)
    return np.concatenate(x_res), np.concatenate(y_res)


def RMSE(df_1, df_2, cols, labels=None):
    x, y = process(df_1, df_2, cols, labels=labels)
    return rmse(x, y)


def rmse(x, y, r=3):
    return round(np.sqrt(sum(np.square(x - y)) / len(x)), r)


def MAE(df_1, df_2, cols, labels=None):
    x, y = process(df_1, df_2, cols, labels=labels)
    return mae(x, y)


def mae(x, y, r=3):
    return round(np.mean(np.abs(x - y)), r)


def pearson(x, y):
    return scipy.stats.pearsonr(x, y)


def precision(X, y, cols , anomaly=1, **kwargs, ):
    X, y = np.array(X,dtype=int)[:,cols], np.array(y,dtype=int)[:,cols]
    assert anomaly in X , f'X : {X}'
    assert anomaly in y , f'y : {y}'
    set_as_anomaly = X == anomaly
    real_anomalies = y == anomaly
    true_positive = np.sum(X[real_anomalies] == anomaly)
    pres =   true_positive / np.sum(set_as_anomaly)
    return pres



def anomaly_confusion_matrix(injected, truth, repair, labels=[]):
    """
    returns cm , plot_func
    the confusion matrix and function that directly returns the plot
    to avoid having multiple plots
    plot_func() -> plt
    """
    injected = np.array(injected)
    non_labeled = np.ones_like(injected, dtype=bool)
    non_labeled[labels] = False
    injected = injected[non_labeled]
    truth = np.array(truth)[non_labeled]
    repair = np.array(repair)[non_labeled]
    true_anomalies = np.invert(np.isclose(injected, truth))
    predicted_anomalies = np.invert(np.isclose(injected, repair))
    cm = sm.confusion_matrix(true_anomalies, predicted_anomalies)
    return cm, lambda: confusion_matrix_plot(cm)


def confusion_matrix_plot(cm):
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(x=j, y=i, s=cm[i, j], va='center', ha='center', size='xx-large')

    plt.xlabel('Predicted', fontsize=20)
    plt.ylabel('Actuals', fontsize=20)
    plt.title('Confusion Matrix', fontsize=18)
    plt.yticks([0, 1], ["Normal", "Anomaly"], rotation=90, fontsize=15)
    plt.xticks([0, 1], ["Normal", "Anomaly"], fontsize=15)
    ax = plt.gca()
    ax.tick_params(axis="x", bottom=True, labelbottom=True, labeltop=False, top=False)
    return plt


def get_metrics(injected, truth, repair, labels=[], return_plot=True):
    cm, cm_plot = anomaly_confusion_matrix(injected, truth, repair, return_plot=return_plot, labels=labels)
    original_rmse = RMSE(injected, truth, labels=labels)
    rmse = RMSE(injected, truth, labels=labels)

    return {"confusion_matrix": cm, "confusion_matrix_plot": cm_plot, "original_rmse": original_rmse, "rmse": rmse}
