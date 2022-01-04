import numpy as np
import pandas as pd

from Repair.Algorithms_File import  RPCA
from sklearn import linear_model

from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from Repair.res.timer import Timer


def add_features(shift, window, X):
    shifts = [X.shift(i, fill_value=0) for i in range(shift+1) if i != 0 ]
    window_df = X.rolling(window, min_periods=1).mean()
    return pd.concat([X] + shifts + [window_df], axis=1)



def RPCA_lindmod(injected, cols ,n_components=1, threshold=2.2, **kwargs):
    timer = Timer()
    timer.start()
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass

    injected = injected.copy()
    model = Robust_PCA_estimator(delta=0.061, n_components=1, threshold=threshold, shift=10)

    np.random.seed(100)
    sampled = injected.sample(n=1000, axis='rows', replace=True)
    model.fit(sampled)
    reduced_data = pd.DataFrame(model.predict(injected))


    repair = injected.copy()

    for col in cols:
        reduced = reduced_data.iloc[:, col]
        reduced = add_features(1, 10, reduced)
        reduced[2] = np.array(injected.index)

        lr = linear_model.HuberRegressor(epsilon=1.01)
        lr.fit(reduced, injected.iloc[:, 0])
        linear_predicted = lr.predict(reduced)

        to_repair_col = np.array(injected.iloc[:, col].copy())

        diff = linear_predicted - to_repair_col
        mean = np.mean(diff)
        std = np.std(diff)
        abs_z_score = diff * 0 if std == 0 else abs((diff - mean) / std)

        to_repair_booleans = abs_z_score > threshold

        to_repair_col[to_repair_booleans] = linear_predicted[to_repair_booleans]
        repair.iloc[:,col] = to_repair_col




    return {"repair": repair, "runtime": timer.get_time() ,"n_components" : n_components
        , "threshold" : threshold ,"type":RPCA}
