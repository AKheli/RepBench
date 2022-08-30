import pandas as pd
from algorithms.estimator import Estimator

x = pd.DataFrame([[1,-10,1,1,1,2,3,4,1]]).T
y = pd.DataFrame([[1,1,1,1,1,1,1,1,1]]).T
predicted = pd.DataFrame([[1,-10,-10,1,1,2,3,1,1]]).T
L = pd.DataFrame([[True,True,False,False,False,True,False,False,False]]).T

mae = (11+2)/6
full_rmse = (11**2+2**2)/6
full_rmse = full_rmse**(1/2)
partial_rmse = ((2**2)/2)
partial_rmse = partial_rmse**(1/2)

e = Estimator(1)
print(e.scores(x,y,L,predicted))
print(mae,full_rmse,partial_rmse)