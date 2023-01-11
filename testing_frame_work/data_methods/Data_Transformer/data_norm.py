folder = "data/test"
import os
import pandas as pd
#z score normalize each dataset in the folder
try:
    os.mkdir("data/test_norm")
except:
    pass
for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(folder+"/"+file)
        df = (df - df.mean())/df.std()
        df.to_csv("data/test_norm/"+file, index=True,index_label="x")

