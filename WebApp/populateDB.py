from WebApp.viz import datasetsConfig
from WebApp.viz.models import DataSet
import pandas as pd

info = datasetsConfig.data_sets_info

for k, v in info.items():
    path = v.pop('path')
    dataset = pd.read_csv("data/" + path).to_json()
    v["title"] = k
    if not DataSet.objects.filter(title=k).exists():  # update with this title
        DataSet.objects.create(dataframe=dataset, **v)
    else:
        DataSet.objects.filter(title=k).update(dataframe=dataset, **v)
    v["path"] = path
