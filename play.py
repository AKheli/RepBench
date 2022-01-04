import numpy as np
import random
x = np.arange(1,16,).reshape(3,-1)

c = np.array([[1,0,-1,0,20]])
c = c/np.sqrt(np.sum(c**2))
c = np.dot(c.T,c)

p = np.eye(5)-c
np.sqrt(np.diag(x.dot(p.dot(x.T)).T))
np.linalg.norm(x-np.dot(x,c.T),axis=1)


import time
from decimal import Decimal
l = random.choices([True]*1000+[list(range(100000))]*30000, k=1000000)
start = time.time()

l = [i for i in l if not i == True]

print(time.time()-start)

l2 = l.copy()
l = random.choices([True]*1000+[list(range(100000))]*30000, k=1000000)


l2 = []
for i in range(int(len(l))/1000):
    x = 
    l2 =




reverse_range = list(range(len(l)))[::-1]
start = time.time()
for i in reverse_range:
    if l[i] == True:
        del l[i]
print(time.time()-start)

