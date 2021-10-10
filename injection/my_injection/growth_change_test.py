import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from injection.my_injection.Injector import inject_amplitude_shift, Anomalygenerator, inject_growth_change

##vadetis
df =pd.read_csv('Data/vadetis_injections/SAG_groth_change.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
injection_range = vaditis_injvected[vaditis_injvected["class"] == 1].index
vaditis_injvected = vaditis_injvected["value"]

#injections

##from direct injection
df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
df =df[df["ts_name"] == "SAG"]

original = df["value"]
data = np.array(original)

data1 , _ = inject_growth_change(data,injection_range , factor=10/9 ,directions=[1])


difference = data1 - np.array(vaditis_injvected) # 0
print(sum(difference))
# plt.plot(data1 , linewidth = 5)
# plt.plot(np.array(vaditis_injvected))
# plt.plot(np.array(original))
# plt.show()

# from direction class

injector = Anomalygenerator(original.copy())

injector.add_growth(starting_index= injection_range[0], length = len(injection_range),factor=10/9,directions=[1])

series = injector.get_injected_series()

plt.plot(series ,linewidth = 5)
plt.plot(np.array(original))
#plt.plot(data1,linestyle = "dotted",linewidth = 3)
plt.plot(np.array(vaditis_injvected),linestyle = "dashed")

plt.show()


data = pd.read_csv("Data/stock10k.data", sep="," , header = 0)
data = pd.read_csv("Data/stock10k.data", sep="," , names=list(range(data.shape[1])), header = 0)

injector = Anomalygenerator(np.array(data[2].copy()))

injector = Anomalygenerator(data[2].copy())
injector.add_growth(length=100)

