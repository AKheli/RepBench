import numpy as np

from Repair.Algorithms_File import IMR, ALGORITHM_PARAMETERS
from Repair.IMR.IMR import imr2
from Repair.IMR.label_generator import  generate_random_labels, \
    generate_anomaly_start_labels

import matplotlib.pyplot as plt

from Repair.res.timer import Timer

alg_type = IMR
default_params = ALGORITHM_PARAMETERS[alg_type]
def IMR_repair(injected, truth, cols = [0], params ={},labels = None ,**kwargs):
    timer = Timer()
    p = params.get("p", default_params["p"])
    tau = params.get("tau", default_params["tau"])
    max_itr_n = params.get("max_itr_n", default_params["max_itr_n"])
    label_anom_start = params.get("label_anom_start", default_params["label_anom_start"])
    label_rate = params.get("label_rate", default_params["label_rate"])

    injected = injected.copy()

    injected_cols = np.array(injected.iloc[:, cols])
    truth_cols =    np.array(truth.iloc[:, cols])
    if injected_cols.ndim == 2:
        injected_cols = np.sum(injected_cols,axis=1)
        truth_cols= np.sum(truth_cols,axis=1)
    assert len(injected_cols) == len(injected.iloc[:,0])

    if labels is None:
        anom_start_labels = generate_anomaly_start_labels(injected_cols,truth_cols,start_of_anomaly=label_anom_start)
        labels = generate_random_labels(np.array(injected.iloc[:, 0]), label_ratio=label_rate, first_labels=p + 1, already_labeled=anom_start_labels)

    for col in cols:
        x = np.array(injected.iloc[:, col])
        truth = np.array(truth.iloc[:, col])

        for i in range(500):
            y_0 = x.copy()
            y_0[labels] = truth[labels]
            if not np.allclose(x,y_0):
                break
        if i == 49:
            plt.plot(x)
            plt.plot(truth)
            plt.show()
            assert False , "x and y_0 initialization are to close for a repair"
        timer.start()
        repair_results = imr2(x, y_0, labels, tau=tau, p=p, k=max_itr_n)
        timer.pause()

        repair = injected.copy()
        repair.iloc[:, col] = repair_results["repair"]

    return { "repair" : repair , "labels" : labels , "runtime" : timer.get_time() , "type" : alg_type , "name" : f'{alg_type},({p},{tau})'}


def IMR_repair_random(injected, truth, cols = [0], params ={}, **kwargs):
    return IMR_repair(injected,truth,cols,params={"label_anom_start" : False})


