import json

import numpy as np
from django.http import JsonResponse

error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_RMSE": "RMSE on Anomaly",
            "runtime": "runtime"}

alg_map = {"imr" : "IMR" , "rpca":"RPCA" , "cdrec" :"CDrep" , "screen" : "SCREEN"}



repbench_maps = {}
repbench_maps.update(error_map)
repbench_maps.update(alg_map)

class RepBenchJsonEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default(self, obj):
        if isinstance(obj, str):
            return repbench_maps.get(obj,obj)
        if isinstance(obj, dict):
            return { repbench_maps.get(key,key) if isinstance(key,str) else key :
                         repbench_maps.get(value,value) if isinstance(value,str) else value
                     for key,value in obj.items()
                     }
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return round(float(obj), 3)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, float):
            return round(obj, 3)
        # if np.isnan(obj):
        #     return None
        return super().default(obj)




def RepBenchJsonRespone(response_data):
    dumped = json.dumps(response_data,cls=RepBenchJsonEncoder)
    # print(type(dumped))
    for k,v in repbench_maps.items():
        # print(k,v)
        dumped = dumped.replace(k,v)
    response_data = json.loads(dumped)
    return JsonResponse(response_data, encoder=RepBenchJsonEncoder)#json_dumps_params={'cls': RepBenchJsonEncoder}
