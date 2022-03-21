import numpy as np


def min_max(x,threshold):
    x_abs = np.abs(x)
    x_normalized= (x_abs -min(x_abs) ) /(max(x_abs ) -min(x_abs))
    return x_normalized > threshold

def z_score(x,threshold):
    x_abs = np.abs(x)
    x_normalized= (x_abs -min(x_abs) ) /(max(x_abs ) -min(x_abs))
    return x_normalized > threshold

def difference_classify(diff_matrix, threshold):
    m = diff_matrix.shape[1]
    anomaly_matrix = np.zeros_like(diff_matrix)

    for i in range(m):
        anomaly_matrix[:,i] = min_max(diff_matrix[:,i],threshold)

    return anomaly_matrix