import os
import os.path as path
import pandas as pd



def has_header(df):
    pass

def train_test_split(split = 0.5):

    for file_name in os.listdir(f"../../data"):
        file_path = f"../../data/"+file_name
        if file_name.endswith(".py") or path.isdir(file_path):
            continue

        try:
            df = pd.read_csv(file_path)
            n,m = df.shape
            split_index = int(n*split)
            test ,train = df.iloc[:split_index,], df.iloc[split_index:,]
            test.to_csv(f"../../data/test/{file_name}")
            train.reset_index()
            train.to_csv(f"../../data/train/{file_name}", index=False)
            test.to_csv(f"../../data/test/{file_name}", index=False)


        except Exception as e:
            if not file_name.endswith(".py"):
                print(f"{file_name} could not be parsed as dataframe")
                raise e
train_test_split()