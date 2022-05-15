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


def get_df_from_file(filename , folder = "Data" ):
    set_path_to_MA()
    file_path = f"{folder}/{filename}"
    data = pd.read_csv(file_path, nrows=0, header=0, sep="," )
    header = None
    for i in data.columns:
        try:
            float(i)
        except:
            header = 0
    data =pd.read_csv(file_path, header=header, sep=",")

    return data , filename


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
