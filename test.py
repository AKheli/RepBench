
import numpy as np
from main import local

## testing the local method


def string_to_series(str, hastruth = True):
    l = str.split(" ")
    return np.array(l[::3]).astype(np.float64) ,  np.array(l[1::3]).astype(np.float64) ,  np.array(l[2::3]).astype(np.float64)

time , val , t = string_to_series('12807 71.16 71.16 12808 70.32 70.32 12809 71.5 71.5 12810 71.5 71.5 12811 71.3 71.3 12812 71.3 71.3 12813 73.49 73.49')
ptime , pval   = (lambda x : ((x[0])[0], (x[1])[0])) ( string_to_series("12806 70.88 70.88"))
ktime , kval   = (lambda x : ((x[0])[0], (x[1])[0])) ( string_to_series("12807 71.16 71.16"))

print(local(time ,  val ,ptime , pval, ktime, kval ))
