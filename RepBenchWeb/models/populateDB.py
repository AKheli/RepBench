from RepBenchWeb.models import DataSet, datasetsConfig
import pandas as pd

data_sets_info = {**datasetsConfig.data_sets_info}
for k, v in data_sets_info.items():
    try:
        print("k")
        path = v.pop('path')
        data = pd.read_csv("data/" + path)
        dataset = data.to_json()
        v["title"] = k
        if not DataSet.objects.filter(title=k).exists():  # update with this title
            DataSet.objects.create(dataframe=dataset, **v)
        else:
            DataSet.objects.filter(title=k).update(dataframe=dataset, **v)
        v["path"] = path
    except Exception as e:
        print(e)





