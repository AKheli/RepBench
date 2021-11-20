import os
import pandas as pd

folder_name = "injection"
def set_path_to_injection():
    current_path = __file__
    print(current_path)
    splitted = current_path.split(folder_name)
    os.chdir("".join(splitted[:-1]) + folder_name)

#search file in data folder or orignal folder
def searchfiles(filename):
    set_path_to_injection()
    filepath = None
    if filename in os.listdir("Data/original"):
        print("in orignal folder")
        filepath =  f"Data/original/{filename}"
    elif filename in os.listdir("Data"):
        print("in data folder")
        filepath = f"Data/{filename}"
    else:
        assert False , "file not found in Injection/Data/original or Injection/Data"

    print(filepath)
    if not os.path.isdir(filepath):
        return [filepath]
    else:
        #todo
        pass


def get_df_from_file(filename):
    set_path_to_injection()
    data = pd.read_csv(filename, nrows=0 , header=0 , sep = None)
    header = None
    for i in data.columns:
        try:
            float(i)
            pass
        except:
            header = 0
    #print("header", header ,data.columns)
    return pd.read_csv(filename,header=header, sep = None) , filename.split("/")[-1]



def get_parameters_from_file(filename='Parameters'):
    set_path_to_injection()
    print("DIRECTORY" , os.listdir())
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


