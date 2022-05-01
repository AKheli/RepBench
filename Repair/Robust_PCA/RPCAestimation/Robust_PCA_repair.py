import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from Repair.algorithms_config import RPCA, ALGORITHM_PARAMETERS
from Repair.Robust_PCA.robust_PCA_estimator import Robust_PCA_estimator
from Repair.res.timer import Timer
import warnings

# transforming
from Scenarios.metrics import RMSE

warnings.simplefilter("ignore", UserWarning)  # feaure name

alg_type = RPCA
default_params = ALGORITHM_PARAMETERS[alg_type]


def RPCA_repair(injected, cols,  n_components=1, threshold=2.2, window = False, **args):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass
    timer = Timer()
    timer.start()
    np.random.seed(100)
    PCA_method = args.get("PCA_method","TruncatedSVD")
    pca = Robust_PCA_estimator(cols=cols, n_components=n_components, threshold=threshold , component_method= PCA_method)
    sampled = injected.sample(n=1000, axis='rows', replace=True)
    pca.fit(sampled)
    repair = pd.DataFrame(pca.predict(injected))
    repair.columns = list(injected.columns)

    return {"repair": repair, "runtime": timer.get_time(), "n_components": n_components,"reduced": pca.reduced_
        , "threshold": threshold, "C" :  pca.components , "type": alg_type  , "name" : f'RPCA({n_components},{round(threshold,2)},{PCA_method})'}



def RPCA_repair_window(injected, cols, n_components=1, threshold=2.2, **args):
    try:
        injected = injected.drop("class", axis=1)
    except:
        pass
    repair = injected.copy()

    window_size = 2000
    total_size = len(injected)

    timer = Timer()
    timer.start()
    PCA_method = args.get("PCA_method","TruncatedSVD")
    pca = Robust_PCA_estimator(cols=cols, n_components=n_components, threshold=threshold , component_method= PCA_method)

    for i in range(max(1,int(total_size/window_size))):
        # repair.plot()
        # plt.show()
        if i == int(total_size/window_size):
            X_window = repair.iloc[i*window_size:,:]
            pca.fit(X_window)
            plt.gca().set_prop_cycle(None)
            comp = list(pca.components_[0,:])
            for c in comp:
                plt.plot(i,c,marker="x")
            repair.iloc[i * window_size:, :] = pd.DataFrame(pca.predict(X_window))
        else:
            X_window = repair.iloc[i * window_size:(i+1)*window_size, :]
            pca.fit(X_window)

            plt.gca().set_prop_cycle(None)
            comp = list(pca.components_[0, :])
            for c in comp:
                plt.plot(i, c, marker="x")
            repair.iloc[i * window_size:(i+1)*window_size, :] = pd.DataFrame(pca.predict(X_window))
    plt.show()

    return {"repair": repair, "runtime": timer.get_time(), "n_components": n_components
        , "threshold": threshold, "type": alg_type  , "name" : f'RPCA({n_components},{round(threshold,2)},_window)'}





