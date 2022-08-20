from skopt import gp_minimize

from parameterization.estimator_optimizer import EstimatorOptimizer


class BayesianOptimizer(EstimatorOptimizer):

    @staticmethod
    def convert_to_range(param_grid):
        param_ranges = {}

        # convert list to ranges
        for k, params_list in param_grid.items():
            if len(set(params_list)) == 1:
                param_ranges[k] = [params_list[0]]

            else:
                try:
                    [float(i) for i in params_list]  # check if all items are numerical arguments
                    param_ranges[k] = (min(params_list), max(params_list))
                except:
                    param_ranges[k] = params_list

        return param_ranges


    def search(self, repair_inputs,  param_grid):
        param_ranges = self.convert_to_range(param_grid)
        param_keys, param_values = param_ranges.keys(), param_ranges.values()

        self.counter = 0
        import sys
        def f(x):
            self.counter += 1
            sys.stdout.write(f"\rbayesian opt search {self.counter / 30 * 100:.1f} %", )
            estim = self.estim_change_copy(dict(zip(param_keys, x)))
            score= estim.scores(**repair_inputs)[self.error_score]
            return score

        x = gp_minimize(f, param_values, n_jobs=-1,
                        n_calls=30,
                        n_initial_points=20,
                        n_restarts_optimizer=2,
                        ).x

        return dict(zip(param_keys, x))