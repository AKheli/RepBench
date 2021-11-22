import json
import os
import pandas as pd

folder_name = "Repair"


def set_path_to_Repair():
    current_path = __file__
    print(current_path)
    splitted = current_path.split(folder_name)
    os.chdir("".join(splitted[:-1]) + folder_name)


# search file in data folder or orignal folder

valid_endings = [".csv", ".txt", ".data"]


def get_data(filename):
    name = "".join(filename.split("/")[-1])
    set_path_to_Repair()
    path = "Data/" + filename

    ## case there is a injected original and json_file
    injected = pd.read_csv(f'{path}_injected')
    original = pd.read_csv(f'{path}_original')
    jso = json.load(open(f'{path}.json'))
    results = {"injected": injected, "truth": original, "info": jso, "name": name}
    results["original"] = results["truth"]
    return results

#print(get_data('test/BAFU'))
