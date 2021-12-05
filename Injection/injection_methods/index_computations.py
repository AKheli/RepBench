import math
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
    mid = round(size / 2)
    pos = math.ceil(anom_lenght / 2)
    neg = math.floor(anom_lenght / 2)
    assert mid - neg > 0, "not enough space for anomaly"
    return range(mid - neg, mid + pos)


def get_random_ranges(size, anom_lenght=10, number_of_ranges=1, occupied_indices=[], space_between_anomalies=10):
    try:
        size = len(size)
    except:
        pass

    for i in np.arange(10000):
        candidates = sorted(
            np.random.randint(low = int(space_between_anomalies / 2), high=size - int(space_between_anomalies / 2) - anom_lenght,
                              size=number_of_ranges))
        if number_of_ranges == 1:
            return [range(r, r + anom_lenght) for r in candidates]
        if  min(abs(np.diff(candidates))) > (space_between_anomalies + anom_lenght):
            return [range(r, r + anom_lenght) for r in candidates]

    assert False, "no more space for random anomaly found"


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
