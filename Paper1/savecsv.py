import numpy as np
import pandas as pd
import csv



#paper
# labels = [0, 1, 2, 5,11] #in the paper add +1
# x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8,
# 7.5, 8.5])
# y_k = np.array([6, 5.6, 5.4, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
# y= y_k.copy()

#for copmarison
labels = [0, 1, 2, 5,8,11] #in the paper add +1
x = np.array([6, 10, 9.6, 8.3, 7.7, 5.4, 5.6, 5.9, 16.3, 20.8,
7.5, 8.5])
y_k = np.array([6, 5.6, 5.4, 8.3, 7.7, 5.4, 5.6, 5.9, 6.3, 6.8, 7.5, 8.5])
y= y_k.copy()


labeled = np.array([ i in labels for i in range(len(x)) ],dtype=bool)
df = pd.DataFrame( [ list(range(len(x))) , x , y_k , y, labeled]   ).transpose()
df.to_csv("a.csv" , index=False, header=False)