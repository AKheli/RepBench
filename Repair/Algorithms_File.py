IMR = "IMR"
SCREEN = "SCREEN"
RPCA = "RPCA"
Robust_PCA = RPCA


ALGORITHM_PARAMETERS = {IMR : { "p" : 2 , "tau" : 0.1 , "max_itr_n":  1000,
                            "label_anom_start" : 3 ,"label_rate" : 0.2 },
                        SCREEN : { "smin" : -6 , "smax" : 6  , "T" : 1},
                        RPCA : {"threshold" : 2.2 , "n_components" :2},
                        }

ALGORITHM_COLORS = {IMR : "blue" , SCREEN : "purple" , RPCA : "green" }

ALGORITHM_TYPES = ALGORITHM_PARAMETERS.keys()


def parse_anomaly_name(type_name):
    type_name = type_name.lower()
    if type_name in ALGORITHM_TYPES:
        return type_name
    a_min, v_min = -1, 100
    for algo in ALGORITHM_TYPES:
        x = start_of_(type_name, algo)
        if x < v_min:
            a_min, v_min = algo, x
    assert v_min < 100, f"could not parse aglortihms{type_name}"
    return a_min


def start_of_(str, type):
    if len(str) == 0:
        return 0
    if len(type) == 0:
        return 100

    if str[0] == type[0]:
        return start_of_(str[1:], type[1:])
    else:
        return start_of_(str, type[1:]) + 1


