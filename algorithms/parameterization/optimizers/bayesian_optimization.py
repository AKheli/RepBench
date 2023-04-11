import sys

from skopt import gp_minimize
from algorithms.parameterization.optimizers.estimator_optimizer import EstimatorOptimizer

class BayesianOptimizer(EstimatorOptimizer):
    def __init__(self, estim, error_score, *, n_jobs=6,n_calls=50,n_initial_points=20,n_restarts_optimizer=0 , callback=None):
        self.n_calls = n_calls
        self.n_initial_points = n_initial_points
        self.n_restarts_optimizer = n_restarts_optimizer
        self.callback = callback
        super().__init__(estim, error_score, n_jobs=n_jobs)

    @staticmethod
    def convert_to_range(param_grid):
        param_ranges = {}
        print(param_grid)
        # convert list to ranges
        for k, params_list in param_grid.items():
            if len(set(params_list)) == 1:
                param_ranges[k] = [params_list[0]]

            else:
                try:
                    [float(i) for i in params_list]  # check if all items are numerical arguments
                    min_, max_  = min(params_list), max(params_list)
                    if any([isinstance(elem, float) for elem in params_list ]):
                        param_ranges[k] = (float(min_),float(max_))
                    else:
                        param_ranges[k] = (min_, max_)
                except ValueError:
                    param_ranges[k] = params_list

        return param_ranges


    def search(self, repair_inputs,  param_grid , return_full_minimize_result = False):
        param_ranges = self.convert_to_range(param_grid)
        param_keys, param_values = param_ranges.keys(), param_ranges.values()
        self.counter = 0
        def f(x):
            self.counter += 1
            params = dict(zip(param_keys, x))
            estim = self.estim_change_copy(params)
            score = estim.scores(**repair_inputs)[self.error_score]
            # sys.stdout.write(f"\rBayesian Optimization search {self.counter / self.n_calls * 100:.1f} % {score}", )
            if self.callback is not None:
                self.callback({"params":params, "score":score,"iter":self.counter})
            return score

        gp_result = gp_minimize(f, param_values, n_initial_points=self.n_initial_points,n_calls=self.n_calls+self.n_initial_points,n_jobs=-1)

        x =  gp_result.x
        if return_full_minimize_result:
            return  [dict(zip(param_keys, x_)) for x_ in  gp_result.x_iters]  , gp_result.func_vals
        return dict(zip(param_keys, x))
