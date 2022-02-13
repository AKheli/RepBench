import itertools
from copy import deepcopy
from skopt import dummy_minimize



#chalenge ts not i.i.d
class Grid_Search():
    def __init__(self, clf, param_grid,  n_jobs=-1 , **kargs):
        self.clf = deepcopy(clf) #todo check if this works
        self.n_jobs = n_jobs
        self.param_grid = param_grid
        self.best_params_ = None
        self.best_estimator_ = clf
        self._ParamTuner__name_ = "GridSearch"




    def fit(self, X, y , groups = None):
        self.best_params_ =  grid_search(X, y, self.clf, self.param_grid,self.n_jobs)
        self.clf.__dict__.update(self.best_params_)
        self.best_estimator_ = self.clf.fit(X,y)

def select_data(data, truth, samples, sample_offset=0):
    return data, truth


def grid_search(data, truth, clf, params, samples=-1, n_jobs=-1):
    def f(params):
        model = deepcopy(clf)
        # for k, v in params.items():
        #     setattr(model, k, v)
        model.__dict__.update(params)

        selected_data, selected_truth = select_data(data, truth, samples)
        model.fit(selected_data, selected_truth)
        result = model.score(data, truth)
        return result, params

    keys, values = zip(*params.items())
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
    score = -10000000
    best_params = {}

    for params in permutations_dicts:
        result, params = f(params)
        if result > score:
            score = result
            best_params = params

    return best_params
