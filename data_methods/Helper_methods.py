import os
import pandas as pd

folder_name = "MA"

def set_path_to_MA():
    current_path = __file__
    index = current_path.rindex(folder_name)
    os.chdir( current_path[:index+len(folder_name)])


# search file in data folder or orignal folder
valid_endings = [".csv", ".txt", ".data"]

def display_data_folder():
    set_path_to_MA()
    return os.listdir("Data")


def searchfile(filename, folder = "Data"):
    set_path_to_MA()
    if filename in os.listdir(folder):
        filepath = f"{folder}/{filename}"
    else:
        raise ValueError

    if not os.path.isdir(filepath):
        return filepath

    #todo
    else:
        raise ValueError

def searchfiles(filename):
    "expects comma seperated file names"
    set_path_to_MA()
    return [ searchfile(file) for  file in filename.split(",") ]


def get_df_from_file(filename, rec = True):
    set_path_to_MA()
    try:
        data = pd.read_csv(filename, nrows=0, header=0, sep="," )
        header = None
        for i in data.columns:
            try:
                float(i)
                pass
            except:
                header = 0
        data =pd.read_csv(filename, header=header, sep=",")
    except:
        if rec:
            return get_df_from_file(searchfile(filename=filename) , rec = False)
        assert False, "invalid data file"

    return data , filename.split("/")[-1]


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
