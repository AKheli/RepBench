
import numpy as np
import pandas as pd
#assuming equaly spaced indexes

def interpolate(x,y,labels , alpha = None , beta = 0.2):
    labels = np.concatenate(([1],labels),axis = 0)
    y = np.array(y)
    x = np.array(x)
    labeledpoints = y[labels]
    if alpha is None:
        alpha = max(np.diff(x))/10

    a = np.empty(len(x), dtype = float)
    a.fill(np.nan)
    a[:] = np.nan
    a[labels] = labeledpoints

    interpolated_line =  pd.Series(a).interpolate()
    mindist = np.array([ min(abs(labels-p)) for p in np.arange(len(x))   ])
    print(mindist)
    boundry = alpha+ np.log(beta*mindist+1)/2
    above = x > (interpolated_line+boundry)
    below = x < (interpolated_line-alpha-boundry)
    x_repair = x
    x_repair[above]  =interpolated_line[above]
    x_repair[below] = interpolated_line[below]

    return {"repair" : x_repair , "interline" : interpolated_line, "above": interpolated_line+boundry, "below": interpolated_line-boundry}


