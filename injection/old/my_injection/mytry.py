import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time








df =pd.read_csv('../Avaditis_injection/SAG_medium_growth_change.csv', sep=';', header=0)
vaditis_injvected = df[df["ts_name"] == "SAG"]
value_inje = vaditis_injvected["value"]


injected_plcaes = vaditis_injvected[vaditis_injvected["class"]==1].index


scale = 10
factor = 10/9

iterations = 1000

start = time.time()
counter = 0
for i in range(1):
    df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
    start = time.time()
    injected_plcaes = vaditis_injvected[vaditis_injvected["class"]==1].index
    raw = df[df["ts_name"] == "SAG"].copy()
    raw["injected"] = raw["value"]
    slope = np.random.choice([-1]) *factor * np.arange(10)
    raw.iloc[injected_plcaes[:10],5] += slope
    raw.iloc[injected_plcaes[:10][-1]+1:,5]  += slope[-1]
    counter +=  time.time()-start
    start = time.time()
    a = pd.DataFrame(raw["injected"])
    c = raw
print(counter)
counter = 0
# for i in range(1000):
#     df =pd.read_csv('SAG.csv', sep=';',header=0)
#
#     start = time.time()
#     injected_plcaes = vaditis_injvected[vaditis_injvected["class"]==1].index
#     raw = df[df["ts_name"] == "SAG"].copy()
#
#     slope = np.random.choice([-1]) *factor * np.arange(10)
#     raw.iloc[injected_plcaes[:10],"value"] += slope
#     raw.iloc[injected_plcaes[:10][-1]+1:,"value"]  += slope[-1]
#     counter +=  time.time()-start
#     start = time.time()
# print(counter)
#
# counter = 0
counter = 0
for i in range(1):
    df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
    df = df[df["ts_name"] == "SAG"].copy()

    start = time.time()
    injected_plcaes = vaditis_injvected[vaditis_injvected["class"]==1].index
    raw = np.array(df[df["ts_name"] == "SAG"]["value"])
    slope = np.random.choice([-1]) *factor * np.arange(10)
    raw[injected_plcaes[:10]] += slope
    raw[injected_plcaes[:10][-1]+1:]  += slope[-1]
    df["injected"] = raw

    counter += time.time() - start
    start = time.time()
    u = pd.DataFrame()

print(counter)



#plt.plot(raw["value"])



# plt.plot(raw["injected"],'o', color = "black" )
# plt.plot(value_inje)a
# plt.plot(injected_plcaes , np.repeat(1, len(injected_plcaes)), 'o')
# plt.plot(value_inje[injected_plcaes])
#
# plt.show()

counter = 0
for i in range(10000):
    df =pd.read_csv('Data/SAG.csv', sep=';', header=0)
    df = df[df["ts_name"] == "SAG"].copy()

    start = time.time()
    raw = df[df["ts_name"] == "SAG"]["value"].to_numpy()


    counter += time.time() - start

print(counter)
counter = 0
for i in range(10000):
    df = pd.read_csv('Data/SAG.csv', sep=';', header=0)
    df = df[df["ts_name"] == "SAG"].copy()

    start = time.time()
    raw = np.array(df[df["ts_name"] == "SAG"]["value"])


    counter += time.time() - start

print(counter)