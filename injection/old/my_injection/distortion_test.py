import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Injector import  Anomalygenerator, inject_distortion

##vadetis
df =pd.read_csv('Data/vadetis_injections/SAG_distortion.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
injectedranges = vaditis_injvected[vaditis_injvected["class"] == 1].index
vaditis_injvected = vaditis_injvected["value"]

##from direct injection
df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
df =df[df["ts_name"] == "SAG"]

original = df["value"]
data = np.array(original)

data1 , _ = inject_distortion(data,[893, 894, 895, 896, 897, 898, 899, 900, 901, 902] , factor=9)

difference = data1 - np.array(vaditis_injvected) # 0
assert sum(abs(difference)) < 0.000001

## from direction class

injector = Anomalygenerator(data.copy())

injector.add_distortion(starting_index= injectedranges[0], length = len(injectedranges),factor=9)

series = injector.get_injected_series()

# plt.plot(series ,linewidth = 1)
# plt.plot(np.array(vaditis_injvected),linestyle = "dashed")
# plt.plot(data1,linestyle = "dotted",linewidth = 1)
# plt.show()

assert sum(abs(series-data1)) < 0.000001

injector = Anomalygenerator(np.array(original))
injector.add_amplitude_shift(length=12, number_of_ranges=1)
injector.add_distortion(length=10 , number_of_ranges=3)
injector.add_amplitude_shift(length=12, number_of_ranges=3)
injector.add_growth(length=12, number_of_ranges=1)

#injector.add_amplitude_shift( starting_index=  200,length=1)

injector.anomaly_infos
