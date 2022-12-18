from WebApp.viz import datasetsConfig
from WebApp.viz.models import DataSet , InjectedDataSet
import pandas as pd

info = datasetsConfig.data_sets_info

for k,v in info.items():
    path = v.pop('path')
    dataset = pd.read_csv("data/"+path).to_json()
    DataSet.objects.create(dataframe=dataset,**v)
    v["path"] = path




