"""
helper methods that inject anomalies controlled in equaly spaced
over a ts with fixed training size before it.
(for ts size change measure)
"""
import math

import numpy as np
import matplotlib.pyplot as plt

from Injection.res.Injector import inject_amplitude_shift, inject_distortion, inject_growth_change, Anomalygenerator


def get_index_range(data_size, length, occupied_indices=[], location="random"):
    try:
        data_size = len(data_size)
    except:
        pass

    if location == "center":
        mid = round(data_size / 2)
        pos = math.ceil(length / 2)
        neg = math.floor(length / 2)
        assert mid - neg > 0, "not enough space for anomaly"
        return range(mid - neg, mid + pos)

    if location == "random":
        for i in np.arange(10000):
            candidate = np.random.randint(10, data_size - 10 - length)
            print("cand" , candidate)
            print("occupied" ,occupied_indices)
            if candidate not in occupied_indices and candidate + length not in occupied_indices:
                return range(candidate, candidate+length)

        assert False, "no more space for random anomaly found"


def inject_equal_spaced(data, train=0, n=10, location="center", anomalies_per_block=1, anomalylength=10, anom_type = "amplitude_shift" , blocks = "all" ):
    assert anom_type in Anomalygenerator.anomalies.keys() , f"anomaly type {anom_type} not found , suppoeted are { Anomalygenerator.anomalies.keys()} else modify the injector file"
    anom_func = Anomalygenerator.anomalies[anom_type]
    data = np.array(data, dtype=np.float64)
    data_copy = data.copy()
    l = len(data)
    if train < 1:  # ratio or biggr than one
        train = int(l * train)

    train, to_inject = data[:train], data[train:]
    infos = {}
    counter = 0

    for block , array in enumerate(np.array_split(to_inject, n)):


        occupied_indices = []
        ret = array.copy()
        for j in range(anomalies_per_block):
            if blocks != "all" and block not in blocks:
                continue

            counter += 1
            index_range = get_index_range(array, length=anomalylength
                                          , occupied_indices=occupied_indices,
                                          location=location)
            print(index_range)
            injected, info = anom_func(array,index_range)
            infos[counter] = info
            ret +=  np.array(injected) - array
            occupied_indices += info["index_range"]

        train = np.append(train, ret)


    return train, infos




#
# res, info = inject_equal_spaced(np.arange(3000), train=0.2, n=30, location="center", anomalies_per_block=1 , anom_func=inject_amplitude_shift )
# plt.plot(res)
# plt.show()
