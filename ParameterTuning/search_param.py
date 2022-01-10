from sklearn.experimental import enable_halving_search_cv  # noqa
from sklearn.model_selection import HalvingGridSearchCV , GridSearchCV

from Repair.Robust_PCA.RPCAestimation.Robust_PCA_repair import Robust_PCA_estimator
from ParameterTuning.sklearn_bayesian import bayesian_opt
from Repair.Screen.SCREEN_repair import SCREEN_estimator
from Repair.res.timer import Timer
from Scenarios.Anomaly_Types import AMPLITUDE_SHIFT
from Scenarios.metrics import RMSE
from Scenarios.scenario_types.BaseScenario import BaseScenario
from data_methods.Helper_methods import *

N_JOBS = None
def inject(data, anomaly_type):
    b = BaseScenario(anomaly_type=anomaly_type)
    injected = b.transform_df(data)["full_set"]
    return injected

def output_format(best_params,injected,truth,estimator, timer):
    original_error = RMSE(injected, truth,range(len(injected.columns)))

    best_params.update({"cols" : list(range(len(injected.columns)))})
    for k, v in best_params.items():
        setattr(estimator, k, v)
    best_clf = estimator
    best_clf.fit(injected)
    repair = pd.DataFrame(best_clf.predict(injected))
    error = RMSE(repair, truth,range(len(injected.columns)))
    return  {"params": best_params, "originalRMSE": original_error ,"RMSE": error, "time": timer.get_time(),"estimator": estimator.__str__()}

def paramsearch(data, param_grid, opzimiter, estimator , anomaly_type=AMPLITUDE_SHIFT):
    if isinstance(data, str):
        data = get_df_from_file(data)[0]

    try:
        data.drop("class", axis=1)
    except:
        pass

    #set max component values
    if "n_components" in param_grid.keys():
        param_grid["n_components"] = [x for x in param_grid["n_components"] if x < data.shape[1]]

    injected_data = inject(data, anomaly_type)
    injected = injected_data["injected"]
    truth = injected_data["original"]

    # on all columns
    opt_params = {}
    if any([o.lower().startswith("ha") for o in opzimiter]):
        timer = Timer()
        timer.start()

        clf = estimator
        search = HalvingGridSearchCV(clf, param_grid, n_jobs=N_JOBS,
                                     random_state=0, scoring="neg_root_mean_squared_error").fit(injected, truth)

        best_params = search.best_params_
        opt_params["HalvingGridSearchCV"] = output_format(best_params,injected,truth,clf,timer)

    if any([o.lower().startswith("gr") for o in opzimiter]):
        timer = Timer()
        timer.start()
        clf = estimator
        search = GridSearchCV(clf, param_grid, n_jobs=N_JOBS, scoring="neg_root_mean_squared_error").fit(injected, truth)

        best_params = search.best_params_
        opt_params["GridSearchCV"] = output_format(best_params, injected, truth,clf, timer)

    if any([o.lower().startswith("ba") for o in opzimiter]):
        timer = Timer()
        timer.start()

        model = estimator
        search = bayesian_opt(injected, truth, model, {},param_grid, samples=-1)

        best_params = search.best_params_
        opt_params["BayesianOptimization"] = output_format(best_params, injected, truth,model, timer)

    return opt_params


if __name__ == "__main__":
    param_grid = {
        # "threshold": np.arange(0.5, 3., 0.2),
        "n_components": [ 1]#, 4, 5, 6],
         #"delta": [0.5 ** i for i in range(11)],
       # "component_method": ["TruncatedSVD"]
    }

    search1 = paramsearch("YAHOO.csv", param_grid, ["ba","gr","ha"], Robust_PCA_estimator(cols=[0]))

    param_grid = {
        # "threshold": np.arange(0.5, 3., 0.2),
        "T": [1, 2, 3,4,5,6,7,8,9,10],
        "s" : [2**i for i in range(20)]
        # "component_method": ["TruncatedSVD"]
    }
    search2 = paramsearch("YAHOO.csv", param_grid, ["ba","gr","ha"], SCREEN_estimator(cols=[0,1]))


# redo scenario class??
# look at run injection think about class change