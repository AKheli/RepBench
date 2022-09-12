import numpy as np

from Injection.injection_methods.basic_injections import anomaly_size
from data_methods.data_reader import train_test_read
from Scenarios.AnomalyConfig import AMPLITUDE_SHIFT

import os
os.chdir("../")
train,test = train_test_read("bafu", normalize=True)


def inject_amplitude_shift(data, index_range, factor=1, directions=[1, -1], stdrange=(-100, 100)):
    index_range = list(index_range)
    anom_type = AMPLITUDE_SHIFT

    data = np.array(data, dtype=np.float64)
    index_range = np.array(index_range) if index_range is not "complete" else np.arange(len(data))
    size = anomaly_size(data, indexes=index_range)
    data[index_range] += np.random.choice(directions) * factor * size
    return data, {"type": anom_type, "factor": int(factor),
                  "index_range": [int(index) for index in index_range], "std_range": stdrange}


test_1 = train.iloc[:,0] # single series
test_2 = train.iloc[:,[0,1]] #two series

import matplotlib.pyplot as plt


def inject_amp_shift(data, index_range ,target_mse = 2 , directions = (-1,1)):
    index_range = list(index_range)
    anom_type = AMPLITUDE_SHIFT

    data = np.array(data, dtype=np.float64)
    index_range = np.array(index_range) if index_range is not "complete" else np.arange(len(data))
    size = anomaly_size(data, indexes=index_range)
    up_or_down : int  = np.random.choice(directions)
    data[index_range] += up_or_down*target_mse
    return data , _


for index_range in [range(10,20),range(50,55),range(100,140)]:
    injected ,_= inject_amp_shift(test_1,index_range=index_range)
    plt.plot(injected)
    plt.plot(test_1)
    plt.show()


