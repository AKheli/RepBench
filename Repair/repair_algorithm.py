import pandas as pd

import Repair.algorithms_config as ac
from Repair.Dimensionality_Reduction.CDrec.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
from Repair.estimator import Estimator
from Repair.res.timer import Timer
from Scenarios.metrics import RMSE
import sklearn.model_selection as sk_ms


class RepairAlgorithm:
    optimizer = "gridcv"
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
        to_plot = []
        is_training = False
        is_fitted = False

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

    def train(self, X, y):
        # self.times["fit"] =  timer.get_time()
        # self.times["fit"]["total"] += timer.get_time()

        print("training" , self.alg_type)
        print("train size:", X.shape)
        self.is_training = True

        hash_ = hash(str(X) + str(y))

        if hash_ in self._hashed_train_:
            self.__dict__.update(self._hashed_train_[hash_])
        else:
            param_grid = self.estimator.suggest_param_range(X)
            param_input = {"columns_to_repair" : [self.estimator.columns_to_repair]}
            param_input.update(param_grid)

            if self.optimizer == "gridcv":
                opt = sk_ms.GridSearchCV(self.estimator,param_input)

            # opt = BayesianOptimization(self, self.suggest_param_range(X), n_jobs=1)
            opt.fit(X, y)
            self.estimator = opt.best_estimator_
            #self.__dict__.update(fitted_attr)
            #self._hashed_train_[hash_] = fitted_attr.copy()
            #print(self.get_fitted_attributes())

        assert self.is_training

        self.is_training = False

    def repair(self, X, y=None):
        timer = Timer()
        timer.start()
        repair = self.estimator.predict(X, y)
        return {"repair": pd.DataFrame(repair)
            , "runtime": timer.get_time()
            , "type": self.alg_type
            , "name": str(self.estimator)
            , "params": self.estimator.get_params()
                }
