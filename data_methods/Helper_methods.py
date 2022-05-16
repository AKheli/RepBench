import os
import pandas as pd



def get_df_from_file(filename , folder = "Data" ):
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



