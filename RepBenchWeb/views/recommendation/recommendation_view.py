from django.http import JsonResponse
from django.shortcuts import render

from RepBenchWeb.forms.recommendation_forms import AutomlSettingsForm, RayTuneSettingsForm
from RepBenchWeb.models import InjectedContainer
from RepBenchWeb.utils.encoder import RepBenchJsonRespone
from RepBenchWeb.views.synthetic_dataset_view import SyntheticDatasetView
from injection.injected_data_container import InjectedDataContainer
from testing_frame_work.data_methods.data_class import DataContainer


class RecommendationView(SyntheticDatasetView):
    template = "recommendation.html"
    recommender_file_name = ""

    def get(self, request, setname="BAFU"):
        data_object = InjectedContainer.objects.get(title=setname)
        injected_data_container: InjectedDataContainer = data_object.injected_container
        data_container = DataContainer(injected_data_container.truth)
        df = data_container.original_data
        context = {"setname": setname}
        context["data_info"] =  InjectedContainer.objects.get(title=setname).get_info()
        context["RepBenchWeb"] = int(request.GET.get("RepBenchWeb", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        context["injected_data_set_info"] = self.data_set_info_context(setname)

        context["flaml_settings_form"] = AutomlSettingsForm()
        context["ray_tune_settings_form"] = RayTuneSettingsForm()
        return render(request, self.template, context=context)


    @staticmethod
    def get_recommendation(request,setname):
        data_object = InjectedContainer.objects.get(title=setname)
        output = data_object.recommendation_context()
        return RepBenchJsonRespone(output)

    @staticmethod
    def recommendation_datasets(request=None, type="recommend"):
        context = {}
        context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
                                        for dataSet in InjectedContainer.objects.all() if
                                        dataSet.title is not None and dataSet.title != "" }
        context["type"] = type
        return render(request, 'data_set_options/repairDatasets.html', context=context)
