import numpy as np

from Scenarios.Anomaly_Types import *

def add_anomaly(anomaly_type, data, index_range = [], factor=None, directions=None, stdrange=None):
    params = {name: param for name, param in zip(["factor", "directions", "stdrange"], [factor, directions, stdrange])
              if param is not None}

    if anomaly_type == AMPLITUDE_SHIFT:
        return inject_amplitude_shift(data, index_range, **params)
    if anomaly_type == DISTORTION:
        return inject_distortion(data, index_range, **params)
    if anomaly_type == GROWTH_CHANGE:
        return inject_growth_change(data, index_range, **params)
    if anomaly_type == POINT_OUTLIER:
        pass  # todo
    assert True, "anomaly type not found"


def inject_growth_change(data, index_range, factor=8, directions=[1, -1]):
    anom_type = GROWTH_CHANGE
    data = np.array(data, dtype=np.float64)
    slope = np.random.choice(directions) * factor * np.arange(len(index_range))
    data[index_range] += slope
    data[index_range[-1] + 1:] += slope[-1]
    return data, {"type": anom_type, "factor": int(factor), "index_range": [int(index) for index in index_range]}


def inject_amplitude_shift(data, index_range, factor=8, directions=[1, -1], stdrange=(-10, 10)):
    anom_type = AMPLITUDE_SHIFT

    data = np.array(data, dtype=np.float64)
    index_range = np.array(index_range)
    minimum, maximum = index_range[0], index_range[-1]

    local_std = data[np.arange(max(0, minimum + stdrange[0]), min(maximum + stdrange[1], len(data) - 1))].std()
    data[index_range] += np.random.choice(directions) * factor * local_std
    return data, {"type": anom_type, "factor": int(factor),
                  "index_range": [int(index) for index in index_range], "std_range": stdrange}


def inject_distortion(data, index_range, factor=8):
    anom_type = DISTORTION
    firstelement = index_range[0] - 1
    index_range_extended = [firstelement] + list(index_range)  # to directly start with the distortion
    data = np.array(data, dtype=np.float64)
    data[index_range_extended[1::]] += (data[index_range_extended[1::]] - data[index_range_extended[:-1:]]) * factor
    return data, {"type": anom_type, "factor": int(factor), "index_range": [int(index) for index in index_range]}