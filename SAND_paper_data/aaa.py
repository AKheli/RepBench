import matplotlib.pyplot as plt
import pandas as pd
import io

import numpy as np
SED = np.fromfile("SED.ts",dtype=float,sep='\n')#[10000:11000]
Annotation = np.fromfile("803.dat",sep='\n' ,dtype=int)#[10000:11000]
# , ; \t \n did not work
plt.plot(SED)
plt.show()

plt.plot(SED)
plt.plot(SED[Annotation] , color = "red")
plt.show()


len(SED[SED<np.mean(SED)])

