import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Injector import inject_amplitude_shift, Anomalygenerator

##vadetis
df =pd.read_csv('Data/vadetis_injections/SAG_Amlitude_schift.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
injectedranges = vaditis_injvected[vaditis_injvected["class"] == 1].index
vaditis_injvected = vaditis_injvected["value"]

#2 injections
first_injection = injectedranges[:int(len(injectedranges)/2)]
second_injection = injectedranges[int(len(injectedranges)/2):]

##from direct injection
df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
df =df[df["ts_name"] == "SAG"]

original = df["value"]
data = np.array(original)

data1 , _ = inject_amplitude_shift(data,first_injection , factor=10,stdrange=(-6,6),directions=[1])

data2 , _ = inject_amplitude_shift(data1,second_injection , factor=10 ,stdrange=(-6,6),directions=[1])

difference = data2 - np.array(vaditis_injvected) # 0
assert(sum(abs(difference)) <0.00001)

## from direction class

injector = Anomalygenerator(data.copy())

injector.add_amplitude_shift(starting_index= first_injection[0], length = len(first_injection),factor=10,std_range=(-6,6),directions=[1])
injector.add_amplitude_shift(starting_index= second_injection[0], length = len(second_injection),factor=10,std_range=(-6,6),directions=[1])

series = injector.get_injected_series()

plt.plot(series ,linewidth = 5)
plt.plot(data2,linestyle = "dotted",linewidth = 3)
plt.plot(np.array(vaditis_injvected),linestyle = "dashed")

plt.show()

injector = Anomalygenerator(np.array(original))
injector.add_amplitude_shift( starting_index=  200)
injector.add_growth( starting_index=  200 )

injector.anomaly_infos
