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


def get_anomaly_indices(array_or_size,anom_lenght=10, number_of_ranges=1  ,
                        min_space_anom_len_multiplier = 1,start_at  = 0 ):
    try:
        size = len(array_or_size)
        assert array_or_size.ndim == 1
    except Exception:
        size  = array_or_size
    size = size - start_at
    number_of_free_spaces = number_of_ranges + 1 # freespaces
    spaces = np.ones(number_of_free_spaces,dtype=int)*int(min(anom_lenght,10))
    additional_space = size-sum(spaces)-number_of_ranges*anom_lenght
    assert additional_space >= 0, f"to many anomalies with data size {size} , anomaly size {anom_lenght} " \
                                  f"and min space between anomalies {min_space_anom_len_multiplier*anom_lenght} " \
                                  f"and {number_of_ranges} anomalies"

    probabilities = np.random.uniform(size = number_of_free_spaces)
    probabilities = probabilities/sum(probabilities) # more variable outcomes
    spaces += np.random.multinomial(additional_space , probabilities)

    assert np.cumsum(spaces)[-1] == size -number_of_ranges*anom_lenght, (size,np.cumsum(spaces)[-1],spaces,additional_space)

    result = []
    for anom_n , space  in enumerate(np.cumsum(spaces)[:-1]+start_at):
        start = space
        result.append(np.arange(start,start+anom_lenght))
    return result



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
