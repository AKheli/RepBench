import numpy as np

from Scenarios.AnomalyConfig import *


def anomaly_size(data, indexes):
    start, stop = indexes[0] , indexes[-1]
    local_range = data[np.arange(max(0, start - len(indexes)*3), min(stop+len(indexes)*2, len(data) - 1))]
    global_std = data.std()
    local_std = local_range.std()
    s = (global_std + 3*local_std)/4
    return s*2.5


def add_anomaly(anomaly_type, data, index_range = [], factor=None, directions=None, stdrange=None
                , random_point_outliers = True ):
    params = {name: param for name, param in zip(["factor", "directions", "stdrange"], [factor, directions, stdrange])
              if param is not None}

    if anomaly_type == AMPLITUDE_SHIFT:
        return inject_amplitude_shift(data, index_range, **params)
    if anomaly_type == DISTORTION:
        return inject_distortion(data, index_range, **params)
    if anomaly_type == GROWTH_CHANGE:
        return inject_growth_change(data, index_range, **params)
    if anomaly_type == POINT_OUTLIER:
        if random_point_outliers is True:
            random_indexes = np.random.choice(np.arange(len(data))[5:-2], size = len(index_range) ,replace=False )
            index_range = sorted(random_indexes)
        return inject_point_outlier(data,index_range,**params)
    assert False, "anomaly type not found"

def inject_point_outlier(data, indexes, factor=1, directions=[1, -1], stdrange=(-100, 100)):
    anom_type = POINT_OUTLIER
    data = np.array(data, dtype=np.float64)
    for i in indexes:
        size = anomaly_size(data,indexes=indexes)
        data[np.random.choice(np.arange(len(data))[10:-10])] += np.random.choice(directions) * factor * size

    return data, {"type": anom_type, "factor": int(factor),
                  "index_range": [int(index) for index in indexes], "std_range": stdrange}



def inject_growth_change(data, index_range, factor=1 ,directions=[1, -1]):
    anom_type = GROWTH_CHANGE
    data = np.array(data, dtype=np.float64)
    slope = np.random.choice(directions) * factor * np.arange(len(index_range))
    data[index_range] += slope
    data[index_range[-1] + 1:] += slope[-1]
    return data, {"type": anom_type, "factor": int(factor), "index_range": [int(index) for index in index_range]}


def inject_amplitude_shift(data, index_range, factor=1, directions=[1, -1], stdrange=(-100, 100)):
    anom_type = AMPLITUDE_SHIFT

    data = np.array(data, dtype=np.float64)
    index_range = np.array(index_range)
    size = anomaly_size(data, indexes=index_range)
    data[index_range] += np.random.choice(directions) * factor * size
    return data, {"type": anom_type, "factor": int(factor),
                  "index_range": [int(index) for index in index_range], "std_range": stdrange}


def inject_distortion(data, index_range, factor=8):
    assert len(index_range) > 1 , "distortion index range has to be greater than one"
    anom_type = DISTORTION
    # data_range = data[index_range]
    # median_  = data_range.median()
    # data[index_range] = (data_range - median_)*(factor-1)
    firstelement = index_range[0] - 1
    index_range_extended = [firstelement] + list(index_range)  # to directly start with the distortion
    data = np.array(data, dtype=np.float64)
    size = anomaly_size(data, indexes=index_range)/2
    X = data[index_range]
    indices = np.arange(len(X))
    s  = 0 #, intercept = np.polyfit(indices, X, 1)
    line = indices * s + np.mean(X)
    diff = np.sign(line-X)
    assert np.any(diff != 0)  , "distortion could not be injected"
    data[index_range] += diff*size #(data[index_range_extended[1::]] - data[index_range_extended[:-1:]]) * factor
    return data, {"type": anom_type, "factor": int(factor), "index_range": [int(index) for index in index_range]}
