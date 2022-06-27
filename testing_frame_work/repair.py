import time
import toml
from Repair.estimator import Estimator
from testing_frame_work.estimator_init import init_estimator_from_type



def run_repair(alg_type, params = "default" , * ,columns_to_repair, injected , truth , labels  , runtime_measurements = 1):
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
    for rm in range(runtime_measurements):
        repair = estimator.repair(truth=truth,injected = injected, columns_to_repair=columns_to_repair , labels = labels)
    end = time.time()
    runtime =  (end - start)/runtime_measurements

    scores = estimator.scores(injected, truth, columns_to_repair, labels, predicted=repair)
    retval = {"repair": repair
        , "runtime": runtime
        , "scores": scores
        , "params" : estimator.get_fitted_params()
        }
    return retval


