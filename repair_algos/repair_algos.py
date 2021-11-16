"""
 All the algorithm return a dictionary with theyr information ,
 the repaired vector is stored as 'result'
"""
import numpy as np
from repair_algos.IMR.IMR import imr2
from repair_algos.Screen.Local import screen


def IMR_repair(x, labeled_values, label_indexes, tau=0.1, p=1, k=3):
    x = np.array(x)
    y_0 = x
    if (len(labeled_values) == len(x)):
        labeled_values = np.array(labeled_values)
        y_0[label_indexes] = labeled_values[label_indexes]
    else:
        y_0[label_indexes] = labeled_values
    assert not np.equal(y_0, x)

    return imr2(x, y_0, label_indexes, tau=tau, p=p, k=k)


def SCREEN_repair(x, indexes=None, t=1, smin=-3, smax=3):
    if indexes is None:
        indexes = np.arange(len(x))

    return screen(np.array([indexes, x]).T, datasize=None, T=t, SMIN=smin, SMAX=smax)
