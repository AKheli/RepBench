import numpy as np

def split(truth,injected , col):
    diff = np.array(truth.iloc[:,col]-injected.iloc[:,col])

    current_anomaly = []
    result = []
    for i,v in enumerate(diff):
        if np.isclose(v,0):
            if len(current_anomaly) != 0:
                result.append(np.array([max(current_anomaly[0]-1,0)] + current_anomaly + [i+1]))
                current_anomaly = []
        else:
            current_anomaly.append(i)
    return result
