import os
import pandas as pd




## params
ts_column_name = "ts_name"  # for vadetis
remove = True
delimiter = None  # pandas will try to infer delimiter itself if it is None
current_path = "/"+__file__
print(__file__)
splitted = current_path.split("/")
Data_Transform_path = "".join(splitted[:-1])
try:
    os.chdir(Data_Transform_path)
except:
    pass



def vadetis_csv_to_df(filename, ts_column_name=ts_column_name):
    df = pd.read_csv(filename, sep=delimiter)
    names = list(df[ts_column_name].unique())
    ts_dict = {}

    # classes = np.zeros(len(df[df[ts_column_name] == names[0]]["value"]))
    for name in names:
        ts_dict[name] = list(df[df[ts_column_name] == name]["value"])

    return pd.DataFrame(ts_dict)














def main():
    transform_function = vadetis_csv_to_df

    for file in [f for f in os.listdir() if f[-2:] != "py"]:
        try:
            df = transform_function(file)
            print(f"{file.split('/')[-1]}  file converted")
            print(df.head())
            df.to_csv(f"../Data/{file.split('/')[-1]}", index=False)
            os.remove(file)
        except:
            print(f"{file.split('/')[-1]} not converted")


if __name__ == "__main__":
    main()


