import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from  .helper_methods import get_parameters_from_file
from matplotlib.pyplot import figure
plt.rcParams["figure.figsize"] = (15,8)



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

def get_possible_indexes(anomaly_class_vector, length = 10, distance = 2, type=1 ):
    for i in np.arange(10000):
        candidate = np.random.randint(distance, len(anomaly_class_vector) - length-distance)
        if np.sum(anomaly_class_vector[np.arange(candidate - distance, candidate + length+distance)]) == 0:
            # we found a range
            index_range = np.arange(candidate, candidate+length)
            anomaly_class_vector[index_range] += type
            return index_range, anomaly_class_vector
    print("anomaly density seems already really high in this dataset")


anomalies = {"amplitude_shift" : inject_amplitude_shift  , "distortion" :  inject_distortion , "groth_change"  :  inject_growth_change}

class Anomalygenerator:
    anomalies = anomalies
    def __init__(self, data , parameter_file = "Parameters"):
        self.original_data = data
        self.data = data.copy()
        self.anomaly_indexes = np.zeros(len(data))
        self.anomaly_infos = {}
        self.anomaly_count = 0
        self.individual_anomalies = {}
        self.parameters = get_parameters_from_file(parameter_file)

    def _set_anomaly_range(self,starting_index, length  ):
        if starting_index is None:
            index_range ,self.anomaly_indexes =  get_possible_indexes( self.anomaly_indexes , length ,distance =  self.parameters["general"]["min_space_between_anomalies"] )
        else:
            index_range = np.array(range(starting_index, starting_index+length))
            self.anomaly_indexes[index_range] += 1

        return index_range

    def get_injected_series(self , leave_out_set = []):
        data = self.original_data.copy()
        for key ,value in self.individual_anomalies.items():
            if key not in leave_out_set:
                data += value-self.original_data
        return data

    def __add_anomaly(self,number_of_ranges,starting_index,length, anomaly_function_dependent_of_index_range , type = None):
        for i in range(number_of_ranges):
            self.anomaly_count += 1
            index_range = self._set_anomaly_range(starting_index, length)
            new_anomaly, new_info = anomaly_function_dependent_of_index_range(index_range)
            self.anomaly_infos[self.anomaly_count] = new_info
            self.individual_anomalies[self.anomaly_count] = new_anomaly
            if type is not None:
                self.anomaly_infos[self.anomaly_count]["type"] = type

    def add_growth(self, length=10, factor= 8, starting_index=None,  number_of_ranges=1 ,directions=[1,-1], use_param_file = True):
        if use_param_file:
            params = self.parameters["growth_change"]
            length = params["length"]
            factor = params["factor"]
            starting_index = params["starting_index"] if isinstance(params["starting_index"] , int) else None
            number_of_ranges = params["number_of_injections"]


        self.__add_anomaly(number_of_ranges,starting_index,length,
                            lambda index_range :
                            inject_growth_change(self.original_data ,index_range, factor = factor ,directions=directions))

    def add_amplitude_shift(self, length=10, factor=8, starting_index=None,  number_of_ranges=1 , std_range=(-10, 10),directions=[1, -1],use_param_file = True):
        if use_param_file:
            params = self.parameters["amplitude_shift"]
            length = params["length"]
            factor = params["factor"]
            starting_index = params["starting_index"] if isinstance(params["starting_index"], int) else None
            number_of_ranges = params["number_of_injections"]

        self.__add_anomaly(number_of_ranges, starting_index, length,
                           lambda index_range:
                           inject_amplitude_shift(self.original_data ,index_range, factor = factor , stdrange= std_range,directions=directions))

    def add_distortion(self, length=10, factor=8, starting_index=None, number_of_ranges=1,use_param_file = True):
        if use_param_file:
            params = self.parameters["distortion"]
            length = params["length"]
            factor = params["factor"]
            starting_index = params["starting_index"] if isinstance(params["starting_index"], int) else None
            number_of_ranges = params["number_of_injections"]

        self.__add_anomaly(number_of_ranges, starting_index, length,
                            lambda index_range:
                            inject_distortion(self.original_data, index_range, factor=factor))

    def add_extreme_point(self, length=1, factor=8, starting_index=None, number_of_ranges=1,use_param_file = True):
        if use_param_file:
            params = self.parameters["extremevalue"]
            factor = params["factor"]
            starting_index = params["starting_index"] if isinstance(params["starting_index"], int) else None
            number_of_ranges = params["number_of_injections"]

        length = 1
        self.__add_anomaly(number_of_ranges, starting_index, length,
                            lambda index_range:
                            inject_amplitude_shift(self.original_data, index_range, factor=factor) , type =  "extreme")

    def extend(self,values, length = 1):
        return [values[0]-i for i in range(1,length+1)] + list(values) + [ values[-1] + i for i in range(1,length+1)]

    def plot(self ,legend= False , multidindow =  True):
        data = self.get_injected_series()
        plt.plot(self.original_data, linewidth=2 ,  marker = '.', label="original",color = "black")
        #plt.plot(data, linestyle="" , marker = "." , label="injected")

        for i, value in enumerate(sorted(self.anomaly_infos.values(), key=lambda x: x["index_range"][0])):
            range = self.extend(value["index_range"])
            plt.plot(range, data[range], marker='.', label=value["type"], color="red")
        # if legend:
        #     plt.legend()


        anomaly_number = len(self.anomaly_infos)
        if anomaly_number:
            fig , ax  = plt.subplots(ncols =anomaly_number)
            #fig.set_size(*figsize)
            try:
                ax[0]
            except:
                ax = [ax]

            for i,value in enumerate(sorted(self.anomaly_infos.values() ,key = lambda x : x["index_range"][0])):
                range = self.extend(value["index_range"])
                #plt.plot(range, data[range], linestyle="",  marker = '.' , label = value["type"])
                #plt.xlim(self.extend(range))
                ax[i].set_title(value["type"])
                ax[i].plot(range, self.data[range],  marker = '.' , label = value["type"],color = "black")
                ax[i].plot(range, data[range], marker='.', label=value["type"], color="red")


        plt.show()

    def repair_print(self):
        for i, value in enumerate(sorted(self.anomaly_infos.values(), key=lambda x: x["index_range"][0])):
            range = value["index_range"]
            data = self.get_injected_series()
            print()
            print((pd.DataFrame( { "index" : range, "original": self.data[range] ,"injected" :  data[range]})).to_string(index=False))


    def save(self , name : str):
        name = "Data/generated/"+name
        frame = pd.DataFrame()
        frame["truth"] = self.original_data
        frame["injected"] = self.get_injected_series()
        frame["class"] = self.anomaly_indexes
        frame.to_csv(name)

        with open(name.split(".")[0]  +".json", 'w') as fp:
            json.dump(self.anomaly_infos, fp)


class Multiple_injector(Anomalygenerator):
    def __init__(self, df, col_index,  parameter_file="Parameters"):
        self.df = df
        self.col_index = col_index
        data = np.array(df.iloc[:, col_index])
        Anomalygenerator.__init__(self,data, parameter_file=parameter_file)


    def save(self , name : str):
        name = "Data/generated/"+name
        frame = pd.DataFrame()

        frame["truth"] = self.original_data
        frame["injected"] = self.get_injected_series()
        frame["class"] = self.anomaly_indexes
        for n in self.df.columns:
            if n != self.df.columns[self.col_index]:
                frame[n] = self.df[n]

        frame.to_csv(name)

        with open(name.split(".")[0]  +".json", 'w') as fp:
            json.dump(self.anomaly_infos, fp)