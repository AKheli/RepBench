from django.http import JsonResponse
from django.shortcuts import render

from WebApp.viz.models import InjectedContainer
from testing_frame_work.repair import AnomalyRepairer
from WebApp.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from WebApp.viz.forms.alg_param_forms import SCREENparamForm, RPCAparamForm, CDparamForm, IMRparamField
from WebApp.viz.forms.injection_form import InjectionForm, store_injection_form
import json
from WebApp.viz.ts_manager.HighchartsMapper import map_repair_data
from WebApp.viz.views.dataset_views import DatasetView


def parse_param_input(p: str):
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p


class RepairView(DatasetView):
    template = "repair.html"
    error_map = {"rmse": "RMSE",
                 "mae": "MAE",
                 "partial_rmse": "RMSE on Anomaly",
                 "runtime": "runtime"}

    ParamForms = {"SCREEN": SCREENparamForm(), "RPCA": RPCAparamForm(), "CDrec": CDparamForm(), "IMR": IMRparamField()}

    def get(self, request, setname="BAFU"):
        context, df = self.data_set_default_context(request, setname)
        # context.update(self.data_set_repair_and_injection_context(df))

        context["alg_forms"] = self.ParamForms
        context["store_form"] = store_injection_form
        context["injection_form"] = InjectionForm(list(df.columns))

        return render(request, self.template, context=context)


    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container = injected_container_None_Series(df_norm, injected_series)
        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]

        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if
                         k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}
        repaired_series = map_repair_data(repair, injected_data_container, alg_name, links, df_original)
        output = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        context = {"metrics": output["metrics"]}
        output["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')
        return JsonResponse(output)

    def repair_datasets(request=None):
        context = {}
        context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
                                        for dataSet in InjectedContainer.objects.all() if
                                        dataSet.title is not None and dataSet.title != ""}
        return render(request, 'repairDatasets.html', context=context)
