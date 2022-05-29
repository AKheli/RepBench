import os

import pandas as pd



def has_header(df):
    pass

def train_test_split(split = 0.5):

    for file_name in os.listdir():
        try:
            df = pd.read_csv(file_name)
            n,m = df.shape
            split_index = int(n*split)
            test ,train = df.iloc[:split_index,], df.iloc[split_index:,]
            test.to_csv(f"../../Data/test/{file_name}")
            train.reset_index()
            train.to_csv(f"../../Data/train/{file_name}", index=False)
            test.to_csv(f"../../Data/test/{file_name}", index=False)


        except Exception as e:
            if not file_name.endswith(".py"):
                print(f"{file_name} could not be parsed as dataframe")
                raise e
