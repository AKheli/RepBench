import os
import pandas as pd

folder_name = "MA"


def set_path_to_MA():
    current_path = __file__
    index = current_path.rindex(folder_name)
    os.chdir( current_path[:index+len(folder_name)])


# search file in data folder or orignal folder

valid_endings = [".csv", ".txt", ".data"]


def searchfile(filename):
    if filename in os.listdir("Data"):
        filepath = f"Data/{filename}"
    if not os.path.isdir(filepath):
        return filepath

def searchfiles(filename):
    set_path_to_MA()
    return [ searchfile(file) for  file in filename.split(",")]





def get_df_from_file(filename):
    set_path_to_MA()
    data = pd.read_csv(filename, nrows=0, header=0, sep=None)
    header = None
    for i in data.columns:
        try:
            float(i)
            pass
        except:
            header = 0
    # print("header", header ,data.columns)
    return pd.read_csv(filename, header=header, sep=None), filename.split("/")[-1]


def get_parameters_from_file(filename='Parameters'):
    set_path_to_MA()
    with open(f"Parameter_Files/{filename}") as f:
        lines = f.readlines()

    lines = [line.replace('\n', "") for line in lines if len(line) > 1]
    key = None
    anomaly_dict = {}
    for line in lines:
        if line[0] == "#":
            key = line[1:].lower()
            anomaly_dict[key] = {}
        else:
            words = line.split()
            subkey = words[0].lower()
            value = words[1]
            try:
                value = int(value)
            except:
                try:
                    value = float(value)
                except:
                    pass

            anomaly_dict[key][subkey] = value

    return anomaly_dict
