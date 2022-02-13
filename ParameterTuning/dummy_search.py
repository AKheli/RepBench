from copy import deepcopy
from skopt import dummy_minimize



#chalenge ts not i.i.d
class Dummy_Search():
    def __init__(self, clf, param_grid,  n_jobs=-1 , **kargs):
        self.clf = deepcopy(clf) #todo check if this works
        self.n_jobs = n_jobs
        self.set_param_grid(param_grid)
        self.best_params_ = None
        self.best_estimator_ = clf
        self._ParamTuner__name_ = "dummy_search"

    def set_param_grid(self,paramgrid):
        self.param_grid = {}
        for k , v in paramgrid.items():
            self.param_grid[k]  = (min(v),max(v))  if len(v)>2 else v



    def fit(self, X, y , groups = None):
        gp_minimize_result = dummy_minimize_opt(X, y, self.clf, self.param_grid,self.n_jobs)
        self.best_params_ = { k : v for k,v  in zip(self.param_grid.keys(), gp_minimize_result.x) }
        self.clf.__dict__.update(self.best_params_)
        self.best_estimator_ = self.clf.fit(X,y)

def select_data(data, truth, samples, sample_offset=0):
    return data, truth
    # np.random.seed(20)
    # indexes = np.random.randint(len(data), size=samples, dtype=int)
    # return data.iloc[indexes, :], truth.iloc[indexes, :]
    #

def dummy_minimize_opt(data, truth, clf, params_bounds, scoring , samples=-1, n_jobs=-1):
    """  wrap   """
    x = params_bounds.values()

    def f(x):
        model = deepcopy(clf)
        params = {k: v for k, v in zip(params_bounds.keys(), x)}
        # for k, v in params.items():
        #     setattr(model, k, v)
        model.__dict__.update(params)

        selected_data, selected_truth = select_data(data, truth, samples)
        model.fit(selected_data ,selected_truth )
        result = -model.score(data, truth)
        return result

    return dummy_minimize(f, x)

