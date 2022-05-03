import numpy as np
import pandas as pd

import Repair.algorithms_config as ac
from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.Dimensionality_Reduction.CD.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Repair.estimator import Estimator
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE
import sklearn.model_selection as sk_ms


class RepairAlgorithm:
    optimizer = "bayesian"

    repair_estimators = {"rpca": Robust_PCA_estimator, "screen": SCREEN_estimator, "cdrec": CD_Rec_estimator,
                         "imr": IMR_estimator}

    def __init__(self, estimator_name, columns_to_repair, **kwargs):
        estimator = None

        if estimator_name in (ac.IMR, "imr"):
            estimator = IMR_estimator(columns_to_repair=columns_to_repair, **kwargs)
            self.alg_type = ac.IMR
        if estimator_name in (ac.SCREEN , "screen"):
            estimator = SCREEN_estimator(columns_to_repair=columns_to_repair, **kwargs)
            self.alg_type = ac.SCREEN
        if estimator_name in (ac.RPCA , "rpca"):
            estimator = Robust_PCA_estimator(columns_to_repair=columns_to_repair, **kwargs)
            self.alg_type = ac.RPCA
        if estimator_name in (ac.CDREC , "cdrec"):
            estimator = CD_Rec_estimator(columns_to_repair=columns_to_repair, **kwargs)
            self.alg_type = ac.CDREC

        assert estimator is not None, f'{estimator_name} could not be parsed'

        self.estimator: Estimator = estimator
        self.columns_to_repair_ = columns_to_repair

        self._hashed_train_ = {}
        self.times = {}
        self.times["fit"] = {"total": 0}
        self.times["predict"] = {"total": 0}
        self.train_results = {}

    @property
    def columns_to_repair(self):
        return self.columns_to_repair_

    @columns_to_repair.setter
    def columns_to_repair(self, val):
        print(val)
        #assert isinstance(val,list) , "columns must be a list even when a single collumn is used"
        self.estimator.columns_to_repair = val
        self.columns_to_repair_ = val


    ##evaluation functions
    def error(self, X, y):
        predicted = pd.DataFrame(self.estimator.predict(X))
        original_error = RMSE(X, y, self.columns_to_repair)
        predicted_error = RMSE(predicted, y, self.columns_to_repair)
        return {"original_error": original_error, "error": predicted_error,
                "ratio": predicted_error / original_error}


    def normalize(self,X):
        """
        Parameters: matrix X
        Returns: normalized X , normalization_inverse function
        """
        mean_X, std_X = X.mean(), X.std()
        assert (len(mean_X) , len(std_X)) == (X.shape[1] , X.shape[1])

        def inv_func(X_norm):
            X_norm.columns = X.columns
            result = X_norm*std_X+mean_X
            return result
        return (X-mean_X)/std_X , inv_func

    def train(self,  injected, truth, **kwargs):
        #return
        X,inv = self.normalize(injected)
        y , _ = self.normalize(truth)
        # self.times["fit"] =  timer.get_time()
        # self.times["fit"]["total"] += timer.get_time()

        print("training" , self.alg_type)
        print("train size:", X.shape)
        self.is_training = True

        hash_ = hash(str(X) + str(y))

        if False and hash_ in self._hashed_train_:
            self.__dict__.update(self._hashed_train_[hash_])
        else:
            param_grid = self.estimator.suggest_param_range(X)



            if self.optimizer == "bayesian":
                opt = BayesianOptimization(self.estimator, param_grid)

            param_input = {"columns_to_repair": [ [self.estimator.columns_to_repair]]}
            param_input.update(param_grid)
            print(param_input)
            if self.optimizer == "gridcv":
                opt = sk_ms.GridSearchCV(self.estimator,param_input,cv= zip(range(injected.shape[0]),range(injected.shape[0])))
                #self.train_results = {"name": self.optimizer}.update(opt.cv_results_)

            # opt = BayesianOptimization(self, self.suggest_param_range(X), n_jobs=1)
            opt.fit(X, y)
            self.estimator = opt.best_estimator_


            #self.__dict__.update(fitted_attr)
            #self._hashed_train_[hash_] = fitted_attr.copy()
            #print(self.get_fitted_attributes())

        assert self.is_training

        self.is_training = False


    def repair(self,  injected, truth = None , **kwargs):
        attributes_str = str(self.estimator.get_params())

        X, X_norn_inv = self.normalize(injected)
        y, _ = self.normalize(truth)
        timer = Timer()
        timer.start()
        repair = self.estimator.predict(X, y)
        repair = pd.DataFrame(repair) # *std_X+mean_X
        repair = X_norn_inv(repair)

        assert attributes_str == str(self.estimator.get_params()) , f'{attributes_str} \n {str(self.estimator.get_params())}'
        return {"repair": repair
            , "runtime": timer.get_time()
            , "type": self.alg_type
            , "name": str(self.estimator)
            , "params": self.estimator.get_fitted_params()
            }




