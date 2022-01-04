import math
import random

import numpy as np


def get_index_range(data_size, length, occupied_indices=[], location="random", space_between_anomalies=10):
    try:
        data_size = len(data_size)
    except:
        pass

    if location == "center":
        return get_center(data_size, length)

    if location == "random":
        return get_random_ranges(data_size, length, occupied_indices, space_between_anomalies)


def get_center(size, anom_lenght = 10):
    try:
        size = len(size)
    except:
        pass

    mid = round(size / 2)
    pos = math.ceil(anom_lenght / 2)
    neg = math.floor(anom_lenght / 2)
    assert mid - neg > 0, "not enough space for anomaly"
    return range(mid - neg, mid + pos)


def get_random_ranges(size, anom_lenght=10, number_of_ranges=1, occupied_indices=[], space_between_anomalies=10 , seed = 100):
    try:
        size = len(size)
    except:
        pass
    min_splitsize = anom_lenght+space_between_anomalies
    n_splits = int(size/min_splitsize)
    splits = np.array(np.array_split(np.arange(size),n_splits))
    assert len(splits) >= number_of_ranges , "not enough space for anomalies"
    np.random.seed(seed)
    choosen_splits_i = np.random.choice(np.arange(len(splits)),number_of_ranges,False)
    choosen_splits = splits[choosen_splits_i]
    ranges =  [ split[-anom_lenght:] for split in choosen_splits]

    return ranges



def get_free_spaces(arr):
    arr = np.ones_like(arr) - np.array(arr, dtype=bool)
    results = []
    current = []
    for index, value in enumerate(arr):
        if value:
            current.append(index)
        if not value:
            if len(current) == 0:
                pass
            else:
                results.append(np.array(current))
                current = []
    if len(current) > 0:
        results.append(np.array(current))

    return results
