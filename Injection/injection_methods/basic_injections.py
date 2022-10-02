import numpy as np
from Injection.injection_config import *
from Injection.injection_methods.index_computations import get_random_indices

def inject_point_outlier(data, indexes, factor, directions=(1, -1)):
    data = np.array(data, dtype=np.float64)
    for index in indexes:
        data[index] += np.random.choice(directions) * factor

    return data
# def inject_growth_change(data, index_range, factor ,directions=[1, -1]):
#     anom_type = GROWTH_CHANGE
#     data = np.array(data, dtype=np.float64)
#     slope = np.random.choice(directions) * factor * np.arange(len(index_range))
#     data[index_range] += slope
#     data[index_range[-1] + 1:] += slope[-1]
#     return data, {"type": anom_type, "factor": int(factor), "index_range": [int(index) for index in index_range]}

def inject_amplitude_shift(data, index_range, factor, directions=(1, -1)):
    data[index_range] += np.random.choice(directions) * factor
    return data


def inject_distortion(data, index_range, factor):
    index_before = index_range[0] - 1
    first_element = data[min(index_before,0)]
    data = np.array(data, dtype=np.float64)
    X = data[index_range]
    #line = np.mean(X)
    # diff = np.sign(line-X)
    # for i,d in enumerate(diff): # make sur it goes in one direction
    #     if d == 0:
    #         diff[i] = i%2*2-1
    #     assert np.any(diff != 0)  ,f"distortion could not be injected {X} ,{data}"
    diff = np.diff(data[index_range], prepend  = [first_element])
    data[index_range] += (diff+np.sign(diff)/2)*factor
    return data



injection_mapper = {AMPLITUDE_SHIFT : inject_amplitude_shift,
                    DISTORTION : inject_distortion ,
                    POINT_OUTLIER : inject_point_outlier}

def add_anomalies(original_column,a_type,*, n_anomalies, a_factor, a_len, offset=0, index_ranges = None , fill_na = False,seed=None):
    if seed is not None:
        np.random.seed(seed)

    data_column = original_column.copy()
    if a_type == POINT_OUTLIER:
        a_len = 1

    if index_ranges is None:
        index_ranges = get_random_indices(len(data_column) - 2 * offset, a_len, n_anomalies)
        index_ranges =  [ arr + offset for arr in index_ranges]

    for index_range in index_ranges:
        data_column[index_range] = injection_mapper[a_type](data_column, index_range,factor = a_factor)[index_range]

    if fill_na:
        anoms = np.invert(np.isclose(data_column,original_column))
        to_fill = np.invert(np.convolve(anoms,[True,True,True],"same"))
        data_column[to_fill] = None

    return data_column , index_ranges