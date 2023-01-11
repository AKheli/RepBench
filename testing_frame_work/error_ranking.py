

import os
import pandas as pd
import numpy as np
import re

error = "RMSE"
def is_error_path(path,error):
        return  path.split("/")[-1] == error


result_df = pd.DataFrame()

for i in [ x for x in os.walk("Results") if len(x[0]) > 0] :
        if not is_error_path(i[0],error):
                continue
        value_dict = {"scenario": i[0].split("/")[1], "anomaly_type" :i[0].split("/")[2]
                     , "data" :i[0].split("/")[3]}

        directory = i[0]
        for file in os.listdir(directory):
                try:
                        x = pd.read_csv(f'{directory}/{file}')
                except:
                        continue

                col = list(x.columns)[0]

                error_mean = np.mean([ float(re.findall(r'\S+', i)[-1]) for i in x[col][1:]]   )
                d = {"error" : error_mean , "algorithm" : col.strip()}
                d.update(value_dict)
                result_df = result_df.append(d,ignore_index=True)

max_ = result_df["error"].argmax()
min_ = result_df["error"].argmin()

result_df.groupby("algorithm").median("error").sort_values(by="error")

