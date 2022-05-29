import os

import shutil

error = "anomaly_rmse"

def is_error_path(path,error):
        return  path.split("/")[-1] == error

for i in [ x for x in os.walk("../Results/full") if len(x[0]) > 0]:

        if not is_error_path(i[0],error):
                continue
        path = i[0]
        file_name = f"/{error}.txt"

        scenario =i[0].split("/")[3]
        a_type  = i[0].split("/")[4]
        data = i[0].split("/")[5]

        data_trim = ""
        for c in data:
                if c.isnumeric():
                        break
                data_trim+=c

        data = data_trim

        directory = i[0]
        print(path)
        try:
                os.mkdir(f"{scenario}_{a_type}")
        except:
                pass

        shutil.copyfile(path+file_name,f"{scenario}_{a_type}/{data}_{error}.txt" )
       #for file in os.listdir(directory):