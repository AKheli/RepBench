# import os
#
# import numpy as np
# import pandas as pd
#
#
#
#
# ## params
# ts_column_name = "ts_name"  # for vadetis
# remove = False
# delimiter = None  # pandas will try to infer delimiter itself if it is None
# classes = "common"
# current_path = "/"+__file__
# splitted = current_path.split("/")
# Data_Transform_path = "".join(splitted[:-1])
# try:
#     os.chdir(Data_Transform_path)
# except:
#     pass
#
#
#
# def vadetis_csv_to_df(filename, ts_column_name=ts_column_name , classes = None , drop_anomalies = True):
#     df = pd.read_csv(filename, sep=delimiter)
#     names = list(df[ts_column_name].unique())
#     ts_dict = {}
#
#     # classes = np.zeros(len(df[df[ts_column_name] == names[0]]["value"]))
#     for name in names:
#         ts_dict[name] = list(df[df[ts_column_name] == name ]["value"])
#
#     if classes == "common":
#         ts_dict["class"] = np.zeros_like(ts_dict[names[0]] ,dtype=np.int64)
#         for name in names:
#             ts_dict["class"] += np.array((df[df[ts_column_name] == name]["class"]),dtype=np.int64)
#         ts_dict["class"][ts_dict["class"] > 0 ] = 1
#         ts_dict["class"] = list(ts_dict["class"])
#
#     if classes == "all":
#         for name in names:
#             ts_dict["class_class"] = list((df[df[ts_column_name] == name]["class"]))
#
#
#     return pd.DataFrame(ts_dict)
#
#
#
# def orbits_txt_save(filename):
#     df = pd.read_csv(filename, sep=delimiter , header = None)
#     return df
#
# def main():
#     transform_function = vadetis_csv_to_df
#
#     for file in [f for f in os.listdir() if f[-2:] != "py"]:
#         try:
#             df = transform_function(file)
#             df.to_csv(f"../../Data/{file.split('/')[-1]}", index=False)
#             if remove:
#                 os.remove(file)
#         except Exception as e:
#             print(e)
#             print(os.listdir("../../"))
#             print(f"{file.split('/')[-1]} not converted")
#
# def select_ts_entries_to_create_df(filename , entries , labels ):
#     df = pd.read_csv(filename, sep=delimiter)
#     df = df.iloc[: , entries]
#     df.columns = labels
#     df.to_csv(filename, index=False)
#     #os.remove(filename)
#
#
# if __name__ == "__main__":
#     main()
#     #select_ts_entries_to_create_df("../../Data/stock10k.data", [2], ["truth"])
#
#
