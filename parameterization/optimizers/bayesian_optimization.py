from skopt import gp_minimize
from parameterization.optimizers.estimator_optimizer import EstimatorOptimizer

class BayesianOptimizer(EstimatorOptimizer):

    def __init__(self, estim, error_score, *, n_jobs=6,n_calls=30,n_initial_points=20,n_restarts_optimizer=2):
        self.n_calls = n_calls
        self.n_initial_points = n_initial_points
        self.n_restarts_optimizer = n_restarts_optimizer
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
        import sys

        def f(x):
            self.counter += 1
            estim = self.estim_change_copy(dict(zip(param_keys, x)))
            score= estim.scores(**repair_inputs)["full_rmse"]
            #sys.stdout.write(f"\rbayesian opt search {self.counter / self.n_calls * 100:.1f} % {score}", )
            return score

        gp_result = gp_minimize(f, param_values, n_jobs=-1,
                        n_calls=self.n_calls+self.n_initial_points,
                        n_initial_points=self.n_initial_points,
                        n_restarts_optimizer=self.n_restarts_optimizer,
                        )
        x =  gp_result.x
        if return_full_minimize_result:
            return  [dict(zip(param_keys, x_)) for x_ in  gp_result.x_iters]  , gp_result.func_vals
        return dict(zip(param_keys, x))
