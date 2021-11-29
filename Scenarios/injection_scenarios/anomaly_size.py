import matplotlib.pyplot as plt

from Scenarios.injection_scenarios.block_injector import inject_equal_spaced
import numpy as np




"""2% spaces"""
def spreaded_anomalies(to_inject, anomaly, length = 15):
    data = to_inject.copy()
    injected_sequences = []
    for i in range(4,40,4):
        number_to_inject = len(data)*i/100/length
        injected_sequences.append(inject_equal_spaced(data , n= number_to_inject)[0])
    return injected_sequences

res = spreaded_anomalies(np.arange(1000) , 10)
plt.plot(res)
plt.show()
for i in res:
    plt.plot(i)
    plt.show()


def longer_anomaly(to_inject, anomaly):
    data = to_inject.copy()
    injected_sequences = []
    for i in range(4,40,4):
        injected_sequences.append(inject_equal_spaced(data , n= 1 , anomalylength = int(len(data)*i/100))[0])
    return injected_sequences


res = longer_anomaly(np.arange(1000) , 10)
plt.plot(res)
plt.show()
for i in res:
    plt.plot(i)
    plt.show()