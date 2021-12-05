#todo handle only labeled values but not whole truth? then when should the rmse be done
import numpy as np

from Repair.repair_algos.Algorithms_File import IMR, ALGORITHM_PARAMETERS
from Repair.repair_algos.IMR.IMR import imr2
from Repair.repair_algos.IMR.label_generator import generate_labels

alg_type = IMR
default_params = ALGORITHM_PARAMETERS[alg_type]


def IMR_repair(df, truth_df , cols = [0],  params ={}):
    p = params.get("p", default_params["p"])
    tau = params.get("tau", default_params["tau"])
    max_itr_n = params.get("max_itr_n", default_params["max_itr_n"])
    label_anom_start = params.get("label_anom_start", default_params["label_anom_start"])
    label_rate = params.get("label_rate", default_params["label_rate"])

    df = df.copy()
    for col in cols:
        x = np.array(df.iloc[:,col])
        truth = np.array(truth_df.iloc[:,col])

        for i in range(20):
            labels = generate_labels(x,truth, label_ratio = label_rate  , first_labels = p+1 , start_of_anomaly = label_anom_start)
            y_0 = x.copy()
            y_0[labels] = truth[labels]
            if not np.allclose(x,y_0):
                break
        if i == 19:
          assert False  , "x and y_0 initialization are to close for a repair"

        df.iloc[:,col] = imr2(x, y_0, labels, tau=tau, p=p, k=max_itr_n)["repair"]

    return df