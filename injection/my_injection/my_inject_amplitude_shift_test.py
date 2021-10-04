import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from injection.my_injection.Injector import inject_amplitude_shift, inject_disortion

df =pd.read_csv('Data/SAG_disortion.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
value_inje = vaditis_injvected["value"]
injectedranges = vaditis_injvected[vaditis_injvected["class"] == 1].index

df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
df =df[df["ts_name"] == "SAG"]
original = df["value"]
data = np.array(original)


data= inject_disortion(data,[892,893, 894, 895, 896, 897, 898, 899, 900, 901, 902] , factor=9,stdrange=(-6,6))





#6,6 is used in vaditis
# find = [(i,j,(inject_amplitude_shift(data, second_injection, factor=10, stdrange=(-i, j)) -np.array(value_inje))[934]) for i in range(30) for j in range(30)  ]
#plt.plot(np.arange(1000)[injectedranges-800],np.array(value_inje)[injectedranges] , color = "black" ,marker='o' )

plt.plot(np.array(value_inje)[800:])
plt.plot(data[800:],linestyle='dashed')
plt.plot(np.array(original)[800:])
#plt.plot(np.arange(1000)[injectedranges-800],np.array(value_inje)[injectedranges] , color = "black" ,marker='o' )





#plt.plot(np.arange(1000)[800:][injectedranges-800],np.array(value_inje)[injectedranges] , color = "red")

plt.show()
