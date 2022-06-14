import time
from timeit import Timer

import toml

import Repair.algorithms_config as ac
from Repair.Dimensionality_Reduction.CD.CDRecEstimator import CDRecEstimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.screen_estimator import SCREENEstimator
from Repair.estimator import Estimator
from Repair.estimator_optimizer import EstimatorOptimizer

def init_estimator_from_type(alg_type, params):
    params = {} if params is None else params
    estimator = None
    if alg_type in (ac.IMR, "imr"):
        estimator = IMR_estimator(**params)
    if alg_type in (ac.SCREEN, "screen"):
        estimator = SCREENEstimator(**params)
    if alg_type in (ac.RPCA, "rpca"):
        estimator = Robust_PCA_estimator(**params)
    if alg_type in (ac.CDREC, "cdrec"):
        estimator = CDRecEstimator(**params)
    assert estimator is not None, f'{alg_type} could not be parsed'

    return estimator

def run_repair(alg_type, params = "default" , * ,columns_to_repair, injected , truth , labels  ):
    """
    Parameters
    ----------
    alg_type : str
    injected :  anomalous df
    truth : truth df
    labels : boolean labels used for IMR

     Parameters
    ----------
    dict : { repair : df , runtime :str , scores : dict }
    """

    if params == "default":
        params = {}
    assert isinstance(params,dict) , f"params must be a dictionary or 'default', was {params}"

    estimator : Estimator = init_estimator_from_type(alg_type,params)

    start = time.time()
    repair = estimator.repair(truth=truth,injected = injected, columns_to_repair=columns_to_repair , labels = labels)
    scores = estimator.scores(injected, truth,columns_to_repair,labels, predicted=repair)
    end = time.time()
    retval = {"repair": repair
        , "runtime": end-start
        , "scores": scores
        , "params" : estimator.get_fitted_params()
        }
    return retval


def find_params(alg_type, metric, train_method,repair_inputs , store = False , id =None):
    estimator = init_estimator_from_type(alg_type,params= None)

    print("training", alg_type)
    print("train size:", repair_inputs["injected"].shape)

    param_grid = estimator.suggest_param_range(repair_inputs["injected"])
    estimator_optimizer = EstimatorOptimizer(estimator, train_method, metric)

    optimal_params = estimator_optimizer.find_optimal_params(repair_inputs, param_grid)

    if store:
        assert isinstance(store,str)
        save_train(alg_type,store,optimal_params,id =id)
    return optimal_params



def save_train(alg_type,name, params , id = None):
    if id is None:
        id = name

    path = f"TrainResults/{alg_type}"
    file_name = "train_results.toml"

    try:
        toml_dict = toml.load(f'{path}/{file_name}')
    except :
        toml_dict = {}
        from pathlib import Path
        Path(path).mkdir(parents=True, exist_ok=True)

    params["names"] = [name]
    toml_dict[id] = params

    with open(f'{path}/{file_name}', 'w') as f:
        print(toml_dict)
        toml.dump(toml_dict, f, encoder=toml.TomlNumpyEncoder(preserve=True))



def load_train(alg_type, name , id =None):
    """
    Raises exceptions if parameters can not be found

    Parameters
    ----------
    alg_type : str
    name : str

    Returns : parametrs
    -------
    """

    if id is None:
        id = name

    path = f"TrainResults/{alg_type}"
    file_name = "train_results.toml"

    toml_dict = toml.load(f'{path}/{file_name}')
    params = toml_dict[id]

    current_names = params.get("names",[])

    if name not in current_names:
        params["names"] = current_names + [name]
        with open(f'{path}/{file_name}', 'w') as f:
            toml.dump(toml_dict, f, encoder=toml.TomlNumpyEncoder(preserve=True))

    del params["names"]

    return params


