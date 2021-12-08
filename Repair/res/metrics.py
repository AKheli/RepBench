import numpy as np
import scipy
import sklearn.metrics as sm
import matplotlib.pyplot as plt

def RMSE(x, y, labels=[], r= 3):
    return rms(x, y, labels=labels , r= r)

def rms(x, y, labels=[], r= 3):
    x = np.array(x)
    y = np.array(y)
    labeled_x, labeled_y = x[labels], y[labels]

    return round(np.sqrt(
        (np.sum(np.square(x - y)) - np.sum(np.square(labeled_x - labeled_y)))
        / (len(x) - len(labeled_x))
    ),r)

def pearson(x, y):
    return scipy.stats.pearsonr(x, y)


def anomaly_confusion_matrix(injected , truth , repair  , labels =[]):
    """
    returns cm , plot_func
    the confusion matrix and function that directly returns the plot
    to avoid having multiple plots
    plot_func() -> plt
    """
    injected = np.array(injected)
    non_labeled = np.ones_like(injected,dtype = bool)
    non_labeled[labels] = False
    injected = injected[non_labeled]
    truth = np.array(truth)[non_labeled]
    repair = np.array(repair)[non_labeled]
    true_anomalies = np.invert(np.isclose(injected,truth))
    predicted_anomalies = np.invert(np.isclose(injected,repair))
    cm = sm.confusion_matrix(true_anomalies,predicted_anomalies)
    return  cm , lambda : confusion_matrix_plot(cm)

def confusion_matrix_plot(cm):
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(x=j, y=i,s=cm[i, j], va='center', ha='center', size='xx-large')

    plt.xlabel('Predicted', fontsize=20)
    plt.ylabel('Actuals', fontsize=20)
    plt.title('Confusion Matrix', fontsize=18)
    plt.yticks([0,1],["Normal" , "Anomaly"],rotation=90 , fontsize = 15 )
    plt.xticks([0,1],["Normal" , "Anomaly"], fontsize = 15)
    ax = plt.gca()
    ax.tick_params(axis="x", bottom=True,  labelbottom=True, labeltop=False, top=False)
    return plt




def get_metrics(injected , truth , repair , labels = [] , return_plot = True):
    cm , cm_plot = anomaly_confusion_matrix(injected, truth, repair, return_plot=return_plot, labels=labels)
    original_rmse =  RMSE(injected, truth, labels=labels)
    rmse = RMSE(injected, truth, labels=labels)

    return {"confusion_matrix" : cm , "confusion_matrix_plot" : cm_plot , "original_rmse": original_rmse ,"rmse" : rmse}
