import json
from RepBenchWeb import datasetsConfig
from RepBenchWeb.catch22.catch22_computations import catch_22_features
from RepBenchWeb.models import DataSet
import pandas as pd

info = dict(datasetsConfig.data_sets_info)

for k, v in info.items():
    try:
        path = v.pop('path')
        data = pd.read_csv("data/" + path)
        dataset = data.to_json()
        additional_info = json.dumps(catch_22_features(data))
        v["title"] = k
        if not DataSet.objects.filter(title=k).exists():  # update with this title
            DataSet.objects.create(dataframe=dataset, additional_info = additional_info, **v)
        else:
            DataSet.objects.filter(title=k).update(dataframe=dataset,additional_info=additional_info, **v)
        v["path"] = path
    except Exception as e:
        print(e)

#python3 manage.py shell
#copy this script inside the shell and run it




