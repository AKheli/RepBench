import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
import json

from Injection.injected_data_container import InjectedDataContainer
from algorithms.Dimensionality_Reduction.dimensionality_Reduction_estimator import DimensionalityReductionEstimator
from testing_frame_work.repair import AnomalyRepairer
from WebApp.viz.BenchmarkMaps.repairCreation import injected_container_None_Series
from WebApp.viz.forms.alg_param_forms import RPCAparamForm, CDparamForm
from WebApp.viz.ts_manager.HighchartsMapper import map_repair_data, reverse_norm
from WebApp.viz.views.dataset_views import DatasetView
from WebApp.viz.views.repair_view import RepairView, parse_param_input
from data_methods.data_class import normalize_f


class DimensionalityReductionView(RepairView):
    template = "dimensionalityReductionVisualization.html"
    ParamForms = {"RPCA": RPCAparamForm(), "CDrec": CDparamForm()}

    @staticmethod
    def repair_data(request, setname):
        post = request.POST.dict()
        post.pop("csrfmiddlewaretoken")
        alg_type = post.pop("alg_type")
        threshold = post["threshold"]

        data_container = DatasetView.load_data_container(setname)
        df_norm = data_container.norm_data  # only work with normalized data
        df_original = data_container.original_data
        injected_series = json.loads(post.pop("injected_series"))
        params = {k: parse_param_input(v) for k, v in post.items()}

        injected_data_container: InjectedDataContainer = injected_container_None_Series(df_norm, injected_series)

        repairer = AnomalyRepairer(1, 1)
        repair_retval = repairer.repair_data_part(alg_type, injected_data_container, params)
        repair = repair_retval["repair"]
        scores = repair_retval["scores"]
        data = {"data": [{"name": RepairView.error_map[k], "y": v} for k, v in scores.items() if
                         k in RepairView.error_map.keys()]}
        metrics = list(scores.keys())
        alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
        scores = {"name": alg_name, "colorByPoint": "true", "data": data}

        original_to_injected_links = {inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series}

        repaired_series = map_repair_data(repair, injected_data_container, alg_name, original_to_injected_links,
                                          df_original)
        context = {"repaired_series": repaired_series, "scores": scores, "metrics": metrics}

        context["html"] = render(request, 'sub/scoreviz.html', context=context).content.decode('utf-8')

        ### Extract Reduced Series
        estimator: DimensionalityReductionEstimator = repair_retval["estimator"]

        def z_score(x):
            x_abs = np.abs(x)
            x_normalized_diff = (x_abs - np.mean(x_abs)) / np.std(x_abs)

            return x_normalized_diff
        normalized_injected, _ = normalize_f(injected_data_container.injected)

        reductions = estimator.reduction_per_classification_iter

        context["reductions"] = [
            [{"name": f"{col}_red_{r_iter + 1}",
              "linkedTo": f"{col}_red_{1}" if i != 0 else None,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col]),
              "true_distance": np.mean(np.sqrt(reverse_norm(df_reduced[col], df_original[col]) - df_original[col]))
              }
             for i, col in enumerate(df_reduced.columns) if i in injected_data_container.injected_columns]
            for r_iter, df_reduced in enumerate(reductions) if r_iter in [0,4,9]]
        print("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        print([c[0]["true_distance"] for c in context["reductions"]])

        df_reduced = reductions[-1]
        context["final_reductions"] = \
            [{"name": f"{col}reduced",
              # "linkedTo": col+"repair"+alg_name,
              "data": list(reverse_norm(df_reduced[col], df_original[col])),
              "norm_data": list(df_reduced[col]),
              "diff_norm": list(z_score(df_reduced[col] - normalized_injected[col]))
              if i in injected_data_container.injected_columns else None,
              "threshold": threshold,
              "classified" : list(estimator.anomaly_matrix[:,i]*1)
              }
             for i, col in enumerate(df_reduced.columns) if
             i in injected_data_container.injected_columns]

        Anomalies = injected_data_container.class_df.values
        classified = estimator.anomaly_matrix
        TP = np.sum(np.logical_and(classified,Anomalies))
        TN = np.sum( np.logical_and(~classified,~Anomalies))

        FP = np.sum(classified == 1) - TP
        FN = np.sum( np.logical_and(~classified,Anomalies))
        context["TP"] = TP
        context["FP"] = FP
        context["FN"] = FN
        context["TN"] = TN

        reconstructions_per_repair_iter = estimator.reconstructions_per_repair_iter

        rgba_colors = [ (245, 127, 39) , (245, 226, 39) ,(144, 245, 39), (39, 245, 243),(39, 54, 245, 0.8)]
        rgba_converter = lambda rgb,a : f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{a})"
        def zones(class_col):
            rgb = rgba_colors.pop(0)
            rgba_colors.append(rgb)

            zones = []
            in_anomaly = False
            print(rgba_converter(rgb,0.2))
            for i, c in enumerate(class_col):
                if c == 1 and not in_anomaly:
                    zones.append({"value": i,  "dashStyle": 'dot' , "color": rgba_converter(rgb,0.2)})
                    in_anomaly = True
                elif c == 0 and in_anomaly:
                    zones.append({"value": i, "color": rgba_converter(rgb,1) })
                    in_anomaly = False

            zones.append({"value": i, "dashStyle": 'dot', "color": rgba_converter(rgb, 0.2)})
            return zones


        context["repair_iters"] = [
            [{"name": f"{col}_repair_iter{r_iter + 1}",
              # "linkedTo": f"{col}_red_{1}" if i != 0 else None,
              "data": list(reverse_norm(df_repair[col], df_original[col])),
              "norm_data": list(df_repair[col]),
              "zones" : zones(estimator.anomaly_matrix[:,i]),
                  "zoneAxis": 'x',
              }
             for i, col in enumerate(df_repair.columns) if i in injected_data_container.injected_columns]
            for r_iter, df_repair in enumerate(reconstructions_per_repair_iter) if r_iter in [0,2,5,9]]


        return JsonResponse(context, encoder=DimensionalityReductionView.encoder)