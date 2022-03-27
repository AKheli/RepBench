import math

import numpy as np


# def get_index_range(data_size, length, occupied_indices=[], location="random", space_between_anomalies=10):
#     try:
#         data_size = len(data_size)
#     except:
#         pass
#
#     if location == "center":
#         return get_center(data_size, length)
#
#     if location == "random":
#         return get_random_ranges(data_size, length, occupied_indices, space_between_anomalies)
#
#
# def get_center(size, anom_lenght = 10):
#     try:
#         size = len(size)
#     except:
#         pass
#
#     mid = round(size / 2)
#     pos = math.ceil(anom_lenght / 2)
#     neg = math.floor(anom_lenght / 2)
#     assert mid - neg > 0, "not enough space for anomaly"
#     return range(mid - neg, mid + pos)


def get_anomaly_indices(array_or_size,anom_lenght=10, number_of_ranges=1 , seed = 100 , min_space_anom_len_multiplier = 2 ):
    try:
        size = len(array_or_size)
        assert array_or_size.ndim == 1
    except Exception:
        size  = array_or_size

    min_space_between_anomalies = anom_lenght*min_space_anom_len_multiplier #includes start and end
    non_anomaly_space = size-anom_lenght*number_of_ranges
    additional_space = non_anomaly_space - (number_of_ranges+1)*min_space_between_anomalies
    assert additional_space >= 0 ,  f"to many anomalies with site {size} , anomaly size { anom_lenght} " \
                                    f"and min space between anomalies {min_space_between_anomalies} " \
                                    f"and {number_of_ranges} anomalies" \


    anomaly_free_ranges = number_of_ranges + 1
    #random spaces
    np.random.seed(seed)
    range_count = np.ones(anomaly_free_ranges,dtype=int)*min_space_between_anomalies
    while additional_space > 0:
            range_count[np.random.randint(len(range_count))] += 1
            additional_space -=1
    assert (sum(range_count) + number_of_ranges*anom_lenght) == size

    results = []
    current_index = 0
    for i in range_count[:-1]:
        range_ = np.arange(current_index+i,current_index+i+anom_lenght)
        results.append(range_)
        current_index = current_index + i + anom_lenght
    assert len(results) == number_of_ranges
    return results





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
