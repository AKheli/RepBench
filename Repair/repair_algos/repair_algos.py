"""
 All the algorithm return a dictionary with theyr information ,
 the repaired vector is stored aored as 'repair'
"""
import numpy as np

from Repair.repair_algos.IMR.IMR import imr2
from Repair.repair_algos.Screen.Local import screen


def IMR_repair(x, labeled_values, label_indexes, tau=0.1, p=1, k=3):
    x = np.array(x)
    y_0 = x
    if (len(labeled_values) == len(x)):
        labeled_values = np.array(labeled_values)
        y_0[label_indexes] = labeled_values[label_indexes]
    else:
        assert len(set(label_indexes)) == len(labeled_values) ,  "The labebeled_values have to be" \
                                                                   "the full truth vector or math the labeled " \
                                                                   "indexes in length"
        y_0[label_indexes] = labeled_values
    assert not np.isclose(x,y_0) , "x and y_0 initialization are to close for a repair"

    return imr2(x, y_0, label_indexes, tau=tau, p=p, k=k)



def SCREEN_repair(x, indexes=None, t=1, smin=-3, smax=3):
    if indexes is None:
        indexes = np.arange(len(x))

    return screen(np.array([indexes, x]).T, datasize=None, T=t, SMIN=smin, SMAX=smax)
