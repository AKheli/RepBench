from copy import deepcopy

import numpy as np
from skopt import gp_minimize
import time


# chalenge ts not i.i.d
class BayesianOptimization():
    def __init__(self, clf, param_grid, n_jobs=1, **kargs):
        self.clf = deepcopy(clf)  # todo check if this works
        assert id(self.clf) != id(clf), f'{id(clf)} {id(self.clf)}'
        assert self.clf.is_training ," nope not a good copy"
        self.set_param_grid(param_grid)
        self.best_params_ = None
        self._ParamTuner__name_ = "BayesianOptimization"

        ##internal_params
        self.n_jobs = 1
        self.n_calls = 30
        self.n_initial_points = 20
        self.n_restarts_optimizer = 3
        self.n_points = 1000
        self.acq_func = 'EI'
        self.kappa = 1.96

    def set_param_grid(self, paramgrid):
        self.param_grid = {}
        for k, v in paramgrid.items():
            self.param_grid[k] = (min(v), max(v)) if len(v) >= 2 else v

    def fit(self, X, y, groups=None):
        self.clf = deepcopy(self.clf)
        gp_minimize_result = self.bayesian_opt(X, y, self.clf, self.param_grid, self.n_jobs)
        self.best_params_ = {k: v for k, v in zip(self.param_grid.keys(), gp_minimize_result.x)}
        self.clf.__dict__.update(self.best_params_)
        self.best_estimator_ = self.clf.fit(X, y)
        self.best_estimator_.predict(X,y)
        self.best_score = gp_minimize_result.fun
        return self

    def bayesian_opt(self, data, truth, clf, params_bounds, scoring, samples=-1, n_jobs=1):
        x = params_bounds.values()

        assert not np.isnan(data.values).any() , "data contains nan values"
        assert not np.isnan(truth.values).any() , "truth contains nan values"
        print(params_bounds)

        def f(x):
            model = deepcopy(clf)
            params = {k: v for k, v in zip(params_bounds.keys(), x)}
            # for k, v in params.items():
            #     setattr(model, k, v)
            model.__dict__.update(params)

            selected_data, selected_truth = data.copy(), truth.copy()
            model.fit(selected_data, selected_truth)
            result = -model.score(data, truth)
            return result

        sys.stdout.write('Bayesian Opt Errors')
        minimized =  gp_minimize(f, x, n_jobs=1
                           , n_calls=self.n_calls,
                           n_initial_points=self.n_initial_points,
                           n_restarts_optimizer=self.n_restarts_optimizer,
                           n_points=self.n_points,
                           acq_func=self.acq_func,
                           kappa=self.kappa, callback=animate)
        sys.stdout.write(f'DONE: {minimized.fun}')
        return minimized


#
# if __name__ == "__main__":
#     file_name = searchfile("temp.csv")
#     print(file_name)
#     df = get_df_from_file(file_name)[0]
#     b = BaseScenario()
#     results = b.transform_df(df)["full_set"]
#     truth = results["original"]
#     injected = results["injected"]
#
#     # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     #     print(injected.corr())
#
#     try:
#         truth.drop("class", axis=1)
#         injected.drop("class", axis=1)
#         df = df.drop("class", axis=1)
#     except:
#         pass
#
#     param_grid = {"threshold": list(np.arange(0.5, 3., 0.2)),
#                   "n_components": [1,2],
#                   "delta": [0.5 ** i for i in range(11)],
#                   "component_method" : [  "TruncatedSVD", "svd"   ],
#                     "interpolate_anomalies": [ False,True]
#
#     }
#
#     default_params = {"cols": [0,1,2,3,4,5,6,7,8,9]}
#
#     bayesian_params = bayesian_opt(injected, truth, Robust_PCA_estimator, default_params, param_grid, samples=-1)
#     model_b = Robust_PCA_estimator(**bayesian_params)
#     d, t = select_data(injected, truth, samples=1000)
#     model_b.fit(d)
#     result_b = pd.DataFrame(model_b.predict(injected))
#     truth.plot()
#     plt.show()
#     result_b.plot()
#     plt.show()
#     injected.plot()
#     plt.show()
#     reduced = pd.DataFrame(model_b.reduce(injected))
#     reduced.plot()
#     plt.show()
#

import sys
import os


def animate(res):
    sys.stdout.write(f' {res.func_vals[-1]},')
    sys.stdout.flush()
