import numpy as np




def inject_growth_change(data,timerange,factor, timedifferences = None , directions = [1,-1]):
    data = np.array(data)
    slope = np.random.choice(directions) * factor * np.arange(len(timerange))
    data[timerange] += slope
    data[timerange[-1] + 1:] += slope[-1]
    return data

def inject_amplitude_shift(data,timerange,factor, timedifferences = None , directions = [1] , stdrange = (-10,10)):
    data = np.array(data)
    minimum ,maximum = timerange[0] , timerange[-1]
    local_std =  data[np.arange(max(0,minimum+stdrange[0]) , min(maximum+stdrange[1] ,len(data)-1))].std()
    data[timerange] += np.random.choice(directions) * factor * local_std
    return data


def inject_disortion(data,timerange,factor, timedifferences = None , directions = [1] , stdrange = (-10,10)):
    data = np.array(data)
    data[timerange[1::]] +=  (data[timerange[1::]]-data[timerange[:-1:]])*factor
    return data