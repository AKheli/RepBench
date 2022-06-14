import pandas as pd
import numpy as np
from testing_frame_work.repair import run_repair

df = pd.read_csv("ild3k.data" , header=None)

labels = df.iloc[:,[4]]
truth = df.iloc[:,[3]]
injected = df.iloc[:,[1]]

my_repair = run_repair("imr",params={"tau":0.01, "p":1}, injected=injected,truth=truth,labels=labels,columns_to_repair=[0])["repair"]
true_results = np.genfromtxt("p1delta0.01.csv",delimiter=',')
assert  np.allclose(my_repair.values[:,0],true_results)

my_repair= run_repair("imr",params={"tau":0.5, "p":2}, injected=injected,truth=truth,labels=labels,columns_to_repair=[0])["repair"]
true_results = np.genfromtxt("p2delta0.5.csv",delimiter=',')
assert  np.allclose(my_repair.values[:,0],true_results), sum(abs(my_repair.values[:,0]-true_results))

