from random import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json


def inject_growth_change(data, index_range, factor=8, timedifferences=None, directions=[1, -1]):
    data = np.array(data, dtype=np.float64)
    slope = np.random.choice(directions) * factor * np.arange(len(index_range))
    data[index_range] += slope
    data[index_range[-1] + 1:] += slope[-1]
    return data, {"type" : "growth_change", "factor": int(factor), "index_range": [int(index) for index in index_range]}


def inject_amplitude_shift(data, index_range, factor=8, timedifferences=None, directions=[1, -1], stdrange=(-10, 10)):
    data = np.array(data, dtype=np.float64)
    index_range = np.array(index_range)
    minimum, maximum = index_range[0], index_range[-1]

    local_std = data[np.arange(max(0, minimum + stdrange[0]), min(maximum + stdrange[1], len(data) - 1))].std()
    # print( data[index_range], local_std , factor, np.random.choice(directions))
    data[index_range] += np.random.choice(directions) * factor * local_std
    return data, {"type" :"amplitude_shift" ,"factor": int(factor), "index_range": [int(index) for index in index_range], "std_range": stdrange}


def inject_distortion(data, index_range, factor=8, timedifferences=None):
    firstelement = index_range[0] - 1
    index_range_extended = [firstelement] +list(index_range) #to directly start with the distortion
    data = np.array(data, dtype=np.float64)
    data[index_range_extended[1::]] += (data[index_range_extended[1::]] - data[index_range_extended[:-1:]]) * factor
    return data, {"type" : "distortion" , "factor": int(factor), "index_range": [int(index) for index in index_range]}


# def single_anomaly_dictionary(data, single_anomyl_dict):
#     anomaly_type = single_anomyl_dict.pop("anomaly_type")
#
#     if anomaly_type == "amplitude_shift":
#         return inject_amplitude_shift(data, **single_anomyl_dict)
#
#     elif anomaly_type == "distortion":
#         return inject_disortion(data, **single_anomyl_dict)
#
#     elif anomaly_type == "growth_change":
#         return inject_growth_change(data, **single_anomyl_dict)
#
#     else:
#         print("no valid anomaly type recognized, used: amplitude_shift, distortion or growth_change")


# def inject(data, anomaly_dict):
#     """
#
#     :param data: a data vector
#     :param anomaly_dict:e.g  {"name1" : { "anomaly_type" : "distortion" , "factor" : 8 } , name2 { ...}
#     :return: new data vector with all the inserted anomalies , list of all the anomalies
#     """
#     # check if a single anomaly is given
#     anomaly_type = anomaly_dict.pop("anomaly_type", None)
#
#     if anomaly_type is not None:
#         d, i = single_anomaly_dictionary(data, anomaly_dict)
#         return d, [i]
#
#     anom_infos = []
#     anomaly_data = data.copy()
#     for anomaly in anomaly_dict.keys():
#         single_anomaly_data, anomaly_info = single_anomaly_dictionary(data, anomaly_dict[anomaly])
#         anom_infos.append(anomaly_info)
#         anomaly_data += single_anomaly_data - data
#
#     return anomaly_data, anom_infos


def get_possible_indexes(anomaly_class_vector, length = 10, type=1):
    for i in np.arange(100):
        candidate = np.random.randint(12, len(anomaly_class_vector) - length)
        if np.sum(anomaly_class_vector[np.arange(candidate - 10, candidate + length)]) == 0:
            # we found a range
            index_range = np.arange(candidate, candidate+length)
            anomaly_class_vector[index_range] += type
            return index_range, anomaly_class_vector
    print("anomaly density seems already really high in this dataset")

class Anomalygenerator:
    def __init__(self, data):
        self.original_data = data
        self.data = data.copy()
        self.anomaly_indexes = np.zeros(len(data))
        self.anomaly_infos = {}
        self.anomaly_count = 0
        self.individual_anomalies = {}

    def _set_anomaly_range(self,starting_index, length  ):
        if starting_index is None:
            index_range ,self.anomaly_indexes =  get_possible_indexes( self.anomaly_indexes , length)
        else:
            index_range = np.array(range(starting_index, starting_index+length))
            self.anomaly_indexes[index_range] += 1
            print("range" , index_range)
        return index_range

    def get_injected_series(self , leave_out_set = []):
        data = self.original_data.copy()
        for key ,value in self.individual_anomalies.items():
            if key not in leave_out_set:
                data += value-self.original_data
        return data

    def clear(self):
        self.__init__(self.original_data)

    def delete_anomaly(self, index ):
        self.individual_anomalies.pop(index)
        r = self.anomaly_infos[index]["index_range"].copy()
        self.anomaly_infos.pop(index)
        self.anomaly_indexes[r] -= 1

    def repeat_anomalies(self):
        old_anomalies = self.anomaly_infos.copy()
        self.clear()
        for key, values in old_anomalies.items():
            type = values["type"]

            if type == "growth_change":
                self.add_growth(length = len(values["index_range"]) , factor=values["factor"] )
            if type == "amplitude_shift":
                self.add_amplitude_shift(length = len(values["index_range"]) , factor=values["factor"] ,std_range=values["std_range"])

            if type == "distortion":
                self.add_distortion(length = len(values["index_range"]))


    def __add_anomaly(self,number_of_ranges,starting_index,length, anomaly_function_dependent_of_index_range):
        for i in range(number_of_ranges):
            self.anomaly_count += 1
            index_range = self._set_anomaly_range(starting_index, length)
            new_anomaly, new_info = anomaly_function_dependent_of_index_range(index_range)
            self.anomaly_infos[self.anomaly_count] = new_info
            self.individual_anomalies[self.anomaly_count] = new_anomaly

    def add_growth(self, length=10, factor=1.2, starting_index=None,  number_of_ranges=1 , id = 0 ,directions=[1,-1]):
        self.__add_anomaly(number_of_ranges,starting_index,length,
                            lambda index_range :
                            inject_growth_change(self.original_data ,index_range, factor = factor ,directions=directions))

    def add_amplitude_shift(self, length=10, factor=8, starting_index=None,  number_of_ranges=1 , std_range=(-10, 10),directions=[1, -1]):
        self.__add_anomaly(number_of_ranges, starting_index, length,
                           lambda index_range:
                           inject_amplitude_shift(self.original_data ,index_range, factor = factor , stdrange= std_range,directions=directions))

    def add_distortion(self, length=10, factor=8, starting_index=None, number_of_ranges=1):
        self.__add_anomaly(number_of_ranges, starting_index, length,
                            lambda index_range:
                            inject_distortion(self.original_data, index_range, factor=factor))

    def plot(self ,legend= True):
        data= self.get_injected_series()
        plt.plot(self.original_data, linewidth=2 , label="original")
        plt.plot(data, linestyle="" , marker = "." , label="injected")
        for value in self.anomaly_infos.values():
            range = value["index_range"]
            plt.plot(range, data[range], linestyle="",  marker = '.' , label = value["type"])
        if legend:
            plt.legend()
        plt.show()


    def save(self , name : str):
        name = "Data/generated/"+name
        frame = pd.DataFrame()
        frame["truth"] = self.original_data
        frame["injected"] = self.get_injected_series()
        frame["class"] = self.anomaly_indexes
        frame.to_csv(name)

        with open(name+".json", 'w') as fp:
            json.dump(self.anomaly_infos, fp)


