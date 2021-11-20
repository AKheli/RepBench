import os

import pandas
import pandas as pd
import json
import csv



def set_path_to_top():
    wd = os.getcwd().split("/")
    while wd[-1] != "MA":
        wd = wd[:-1]
    os.chdir('/'.join(wd))


def read_params(filename):
    set_path_to_top()
    with open("evaluation/alg_parameters/"+filename) as csvfile:
        file = csv.reader(csvfile)

        algos = []
        for row in file:
            values = row[0].split()
            if values[0].lower() == "imr":
                algos.append(
                    {"name" : "imr" , "parameters":{ "p" : int(values[1]) , "tau" : float(values[2]) , "k" : int(values[3])}})
            if values[0].lower() == "screen":
                algos.append(
                    {"name": "screen", "parameters": {"T": int(values[1]), "SMAX": float(values[2]), "SMIN": -float(values[2]),}})
        return algos



def search_json(file):
    set_path_to_top()
    folder = "/".join(file.split("/")[:-1])
    l = [ folder +"/"+ x for x in os.listdir(folder) ]
    if  file + ".json" in l:
        return file + ".json"
    if  file.split(".")[0] + ".json" in l:
        return  file.split(".")[0] + ".json"

    assert False , "json file for anomaly position not found"

def anom_dict_from_json(file):
    with open(search_json(file)) as f:
        data = json.load(f)
    return data


#assumed to be in the tool Data folder
# "" all files in Data folder
# file1,file2 file in folder
# folder1,folder2 all filles in folder 1 and folder 2


data_extensions = [".csv", ".Data"]

def files_from_comma_string(files  , folder  = "Data/Injected_data"):
    set_path_to_top()
    output_files = []
    for i in files.split(","):
        path = f'{folder}/{i}'
        if os.path.isdir(path):
            output_files += [ f'{path}/{file}' for file in  os.listdir(path) if file.endswith(tuple(data_extensions))]
        elif path.endswith(tuple(data_extensions)):
            output_files += [path]

    if(len(output_files) == 0):
        print("no file found")
        print(folder)
        print( os.listdir())
    return output_files

#files = files_from_comma_string('amplitude_shift,')


#,truth,injected,class
def get_df_from_file(filename, injected = 1, truth = 2 , labels = 3 ,header = 0 , is_train = False):
    set_path_to_top()
    try:
        df = pd.read_csv(filename, header = 0)
    except:
        print(os.listdir())
        pd.read_csv(filename, header=0)

    if is_train:
        return df

    cols = df.columns
    if "truth" in cols and "injected" in cols:
        cols = list(df.columns)
        cols[0] = "index"
        df.columns = cols
        return df

    truth = None
    injected = None
    index = None

    if ("truth" in cols):
        truth = df["truth"]
        df.drop(columns = "truth" , inplace = True)

    if ("injected" in cols):
        injected = df["injected"]
        df.drop("injected",axis=1, inplace = True)

    cols = df.columns

    #print(np.array(df[cols[0]])[1:]-np.array(df[cols[0]])[:-1])

    if ("labels" in cols):
        return pandas.DataFrame({"index": df[cols[0]], "injected": df[cols[1]] if injected is None else injected,
                                 "truth": df[cols[2]] if truth is None else truth, "labels" : df["labels"]})

    return pandas.DataFrame( {  "index": df[cols[0]] , "injected" :  df[cols[1]] if injected is None else injected,
                         "truth" : df[cols[2]] if truth is None else truth} )



# df = get_df_from_file(files[0])
# print(sum(df["injected"]-df["truth"]))

