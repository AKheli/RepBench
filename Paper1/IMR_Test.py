import numpy as np
import pandas as pd
from IMR import IMR

filename = "a.csv"
data = pd.read_csv(filename,sep=',' , header=None , names=["timn","x" , "y_0","truth", "label"])
test = IMR(np.array(data["x"]),np.array(data["y_0"]),np.arange(len(data["x"]))[np.array(data["label"],dtype=bool)],k=101,p=3)


filename = "ild3k.data"
data = pd.read_csv(filename,sep=',' , header=None , names=["timn","x" , "y_0","truth", "label"])
test = IMR(np.array(data["x"]),np.array(data["y_0"]),np.arange(len(data["x"]))[np.array(data["label"],dtype=bool)],k=101,p=3)


diff = np.mean( np.square((np.array(data["truth"]) - test)[   np.logical_not(np.array(data["label"],dtype=bool))  ])  )
print(diff)
print(diff**(1/2))

#[print(t) for t in test]
