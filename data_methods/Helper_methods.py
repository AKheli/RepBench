import os
import pandas as pd

def get_df_from_file(filename , folder = "Data" ):

    file_path = f"{folder}/{filename}"

    first_row = pd.read_csv(file_path, nrows=1, header=None, sep=",")

    float_in_first_row = any([isinstance(x,float) for x in first_row.values])

    header = None if float_in_first_row else 0


    data =pd.read_csv(file_path, header=header, sep=",")
    # print(data.columns)
    # print(data.iloc[0,:].values)


    return data , filename



