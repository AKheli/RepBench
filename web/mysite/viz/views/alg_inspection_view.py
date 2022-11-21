import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from pandas import DataFrame
import json

from web.mysite.viz.BenchmarkMaps.additional_info_repair import repair_from_None_series_with_additional_info
from web.mysite.viz.BenchmarkMaps.create_repair_output import repair_from_None_series
from web.mysite.viz.views.repair_view import RepairView, parse_param_input


class AlgInspectionView(RepairView):

    def get(self, request, setname="bafu5k"):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_repair_and_injection_context(df))
        return render(request, 'alg_inspection.html', context=context)


    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        df: DataFrame = pd.read_csv(f"data/train/{setname}.csv")
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}
        print(params)
        output = repair_from_None_series_with_additional_info(alg_type, params, df, *injected_series.values())
        context = {"metrics": output["metrics"]}
        output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')

        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                        return obj.tolist()
                if isinstance(obj, pd.DataFrame):
                        return obj.values.tolist()

                return json.JSONEncoder.default(self, obj)

        output = json.loads(json.dumps(output, cls=NpEncoder))


        return JsonResponse(output)


