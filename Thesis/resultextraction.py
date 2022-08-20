import os
import shutil

res_folder = "Results"
res_subfolder = "run_time"
filename = "runtime.txt"

for dirpath, dirnames, filenames in os.walk(f"{res_folder}/{res_subfolder}"):
    for filename_ in filenames:
        if filename_ == filename:
            print(dirpath,dirnames,filename)
            attributes = dirpath.split("/")
            scen, a_type , data_set = attributes[-4:-1]

            new_name = f"{scen}_{a_type}_{data_set}_{filename}"
            shutil.copyfile(f"{dirpath}/{filename_}", f"Thesis/results/{new_name}")