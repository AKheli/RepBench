import numpy as np


def inject_growth_change(data, index_range, factor = 8, timedifferences = None, directions = [1,-1]):
    data = np.array(data , dtype=np.float64)
    slope = np.random.choice(directions) * factor * np.arange(len(index_range))
    data[index_range] += slope
    data[index_range[-1] + 1:] += slope[-1]
    return data ,{ "growth_change" : { "factor" : factor, "index_range" : index_range}}

def inject_amplitude_shift(data, index_range, factor = 8, timedifferences = None, directions = [1,-1], stdrange = (-10, 10)):
    data = np.array(data , dtype=np.float64)
    index_range = np.array(index_range)
    minimum ,maximum = index_range[0] , index_range[-1]

    local_std =  data[np.arange(max(0,minimum+stdrange[0]) , min(maximum+stdrange[1] ,len(data)-1))].std()
    #print( data[index_range], local_std , factor, np.random.choice(directions))
    data[index_range] += np.random.choice(directions) * factor * local_std
    return data , { "amplitude_shift": { "factor": factor, "index_range": index_range, "std_range": stdrange}}


def inject_disortion(data, index_range, factor= 8, timedifferences = None):
    data = np.array(data , dtype=np.float64)
    data[index_range[1::]] += (data[index_range[1::]] - data[index_range[:-1:]]) * factor
    return data , { "distortion": { "factor": factor, "index_range": index_range}}



def single_anomaly_dictionary(data,single_anomyl_dict):
    anomaly_type = single_anomyl_dict.pop("anomaly_type")

    if anomaly_type == "amplitude_shift":
        return inject_amplitude_shift(data, **single_anomyl_dict)

    elif anomaly_type == "distortion":
        return inject_disortion(data, **single_anomyl_dict)

    elif anomaly_type == "growth_change":
        return inject_growth_change(data, **single_anomyl_dict)

    else :
        print("no valid anomaly type recognized, used: amplitude_shift, distortion or growth_change")

def inject(data,anomaly_dict):
    """

    :param data: a data vector
    :param anomaly_dict:e.g  {"name1" : { "anomaly_type" : "distortion" , "factor" : 8 } , name2 { ...}
    :return: new data vector with all the inserted anomalies , list of all the anomalies
    """
    #check if a single anomaly is given
    anomaly_type = anomaly_dict.pop("anomaly_type" , None)

    if anomaly_type is not None:
        d , i = single_anomaly_dictionary(data,anomaly_dict)
        return d, [i]

    anom_infos = []
    anomaly_data = data.copy()
    for anomaly in anomaly_dict.keys():
        single_anomaly_data , anomaly_info = single_anomaly_dictionary(data,anomaly_dict[anomaly])
        anom_infos.append(anomaly_info)
        anomaly_data += single_anomaly_data - data

    return anomaly_data , anom_infos



class anomalygenerator:
    def __init__(self, data):
        pass