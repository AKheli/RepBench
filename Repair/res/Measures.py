import numpy as np
import scipy



def rmse(x, y, labels=[], r= 3):
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