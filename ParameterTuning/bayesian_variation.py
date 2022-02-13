import time
import numpy as np
from skopt import gp_minimize

from ParameterTuning.sklearn_bayesian import BayesianOptimization
from Repair.Robust_PCA.robust_PCA_estimator import Robust_PCA_estimator
from Scenarios.Anomaly_Types import DISTORTION
from Scenarios.scenario_types.BaseScenario import BaseScenario
from Scenarios.scenario_types.Scenario_Constructor_mapper import SCENARIO_CONSTRUCTORS
from Scenarios.scenario_types.Scenario_Types import BASE_SCENARIO
import logging
logging.basicConfig(filename='bayesian.log', level=logging.DEBUG)


internal_params = {"n_initial_points" : [10 ,20 ,30 ,40 ,50 ,100],
            "n_restarts_optimizer" : [0,1,2,3,10],
            "kappa" : (0,4),
            "acq_func" : ["LCB" ,"EI" ,"PI", "gp_hedge"],
            "n_calls" : [50, 100, 200]}

param_grid = {
    "n_components": [1, 2, 3, 4,5,6,7],  # , 4, 5, 6],
    "delta":  np.linspace(0.001,1,num=20),
}

anomaly_type = DISTORTION
data_files = ["YAHOO.csv","batch10.txt" , "TemperatureTS8.csv" , "BAFU20K.txt" ]  # , , "motion_normal.txt", "TemperatureTS8.csv", "BAFU.txt","batch10.txt"]

injection_scenario = SCENARIO_CONSTRUCTORS[BASE_SCENARIO]

training = []
for file in data_files:
    scen = scenario_data = injection_scenario(file, {"anomaly_type" : anomaly_type}, train_test_split=0.5)
    clf = Robust_PCA_estimator(cols=scen.injected_columns)
    train_X , train_y = scenario_data.train["injected"]  ,  scenario_data.train["original"]
    train_X = train_X if train_X.shape[0] <= 5000 else train_X.iloc[:5000,:]
    train_y = train_y if train_y.shape[0] <= 5000 else train_y.iloc[:5000,:]
    training.append((train_X,train_y))



keys , values = internal_params.keys() ,  internal_params.values()
def f(x):
    tuner =  BayesianOptimization(clf, param_grid, n_jobs=-1)
    logging.info(f'{x}')

    print(x)
    try:
        for k , v in zip( keys  ,x):
            assert hasattr(tuner,k)
            setattr(tuner,k,v)
        start = time.time()
        res = [tuner.fit(train_X, train_y).best_score for (train_X , train_y) in training]
        print(res, time.time()-start)
        logging.debug(f'f{res}, {time.time()-start}')
        score = max(res)
    except Exception as e:
        print(e)
        score = 1000
    return score

result  = gp_minimize(f, values, n_jobs=1,n_calls=30,  n_initial_points=20, n_restarts_optimizer=3, n_points=1000,acq_func='EI')

        # BayesSearchCV(clf, param_grid, n_jobs=self.n_jobs,
        #                          random_state=0 )      :
        #     for n_calls in [20, 30, 50, 100, 200]:
        #         try:
        #             print(n_initial_points, kappa, acq_func, n_calls)
        #             t = time.time()
        #             res = gp_minimize(f, x, n_jobs=-1, n_calls=n_calls, kappa=kappa, n_initial_points=n_initial_points,
        #                               n_restarts_optimizer=3, acq_func=acq_func)
        #             print(res.fun)
        #             print(time.time() - t)
        #             with open('bayesiancomp', 'a') as file_:
        #                 file_.write(f'\n{n_initial_points, kappa, acq_func, n_calls}\n')
        #                 file_.write(f'score {res.fun}\n')
        #                 file_.write(f'time {time.time() - t}\n')
        #         except Exception as e:
        #             with open('bayesiancomp', 'a') as file_:
        #                 file_.write(f'{n_initial_points, kappa, acq_func, n_calls} failed')