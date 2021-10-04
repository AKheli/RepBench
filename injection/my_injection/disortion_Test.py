import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from injection.my_injection.Injector import inject_amplitude_shift

df =pd.read_csv('SAG_Amlitude_schift.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
value_inje = vaditis_injvected["value"]
injectedranges = vaditis_injvected[vaditis_injvected["class"] == 1].index

first_injection = injectedranges[:int(len(injectedranges)/2)]
second_injection = injectedranges[int(len(injectedranges)/2):]

df =pd.read_csv('SAG.csv', sep=';', header=0)
df =df[df["ts_name"] == "SAG"]


original = df["value"]
data = np.array(original)
x = data.copy()
data= inject_amplitude_shift(data,first_injection , factor=10,stdrange=(-6,6))

data= inject_amplitude_shift(data,second_injection , factor=10 ,stdrange=(-6,6))
