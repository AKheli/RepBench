import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from injection.my_injection.Injector import Anomalygenerator

data = pd.read_csv('052_UCR_Anomaly_DISTORTEDTkeepThirdMARS_3500_4711_4809.txt', header = None)


injector = Anomalygenerator(np.array(data))
injector.add_distortion(length=100 , factor=2)
injector.plot()
data = injector.get_injected_series()
#plt.plot(data)
plt.plot(range(len(data))[-300+4711:4809+300] , data[-300+4711:4809+300] )
plt.plot(range(len(data))[4711:4809] , data[4711:4809] )

plt.show()
