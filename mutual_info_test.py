import pyinform as pi
import numpy as np
from  sklearn.feature_selection import mutual_info_regression as mi

x = np.random.random(1000)
y = x.copy()
y[10:30] = -y[10:30]
#symetric test
print(mi(x.reshape(-1, 1),y,discrete_features=False,n_neighbors=20))
print(mi(y.reshape(-1, 1),x,discrete_features=False,n_neighbors=20))

x= x.reshape(-1, 1)
y[10:30] = 10
print(mi(x,y,discrete_features=False,n_neighbors=20))

x = np.random.random(1000)
y = x.copy()
y[10:30] = np.random.normal(size=20,scale=0.01)
x= x.reshape(-1, 1)
print(mi(x,y,n_neighbors=20))
print(mi(x,y,discrete_features=False,n_neighbors=20))

# y  = np.array([1]*9+[4.4])
# print(mi(x,y),y)
# #
# # import numpy as np
# # y  = np.random.random(size= 10)
# # print(pi.mutual_info(x,y),y)
# #
# #
# # x = [1,2,3,4,5,6,7,8,9,10]
# # y  = [1,2,3,40,50,6,7,8,9,10]
# # print(pi.mutual_info(x,y),y)
# # y  = [1,2,3,4.0001,5.000001,6,7,8,9,10]
# # print(pi.mutual_info(x,y),y)
# #
# #
# # y  = [1,2,3,5,4,6,7,8,9,10]
# # print(pi.mutual_info(x,y),y)
# # y  = [1]*9+[-1]
# # print(pi.mutual_info(x,y))
