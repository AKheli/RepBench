"""
 All the algorithm return a dictionary with theyr information ,
 the repaired vector is stored aored as 'repair'
"""
import numpy as np

from Repair.repair_algos.IMR.IMR import imr2, imr
from Repair.repair_algos.Screen.Local import screen
from Repair.repair_algos.aglo_helpers import generate_labels

#todo handle only labeled values but not whole truth? then when should the rmse be done
def IMR_repair(x, truth, tau=0.1, p=4, k=10000 , anomaly_info = None):
    x = np.array(x)
    truth = np.array(truth)
    for i in range(20):
        labels = generate_labels(x,0.1,anomaly_info)
        y_0 = x.copy()
        y_0[labels] = truth[labels]
        if not np.allclose(x,y_0):
            break
    if i == 19:
      assert False  , "x and y_0 initialization are to close for a repair"

    output = imr2(x, y_0, labels, tau=tau, p=p, k=k)
    output["name"] = f"IMR({p},{tau})"
    return output




def SCREEN_repair(x, indexes=None, t=1, s = 3):
    if indexes is None:
        indexes = np.arange(len(x))

    output =  screen(np.array([indexes, x]).T, datasize=None, T=t, SMIN=-s, SMAX=s)
    output["name"] = f"SCREEN({t},{s})"
    return output