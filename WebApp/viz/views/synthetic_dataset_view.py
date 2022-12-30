import numpy as np

from Injection.injected_data_container import InjectedDataContainer
from WebApp.viz.views.dataset_views import DatasetView
from WebApp.viz.models import  InjectedContainer
from django.http import JsonResponse
from data_methods.data_class import DataContainer
from WebApp.viz.ts_manager.HighchartsMapper import map_truth_data, map_injected_series


class SyntheticDatasetView(DatasetView):
    template = 'displayDataSetSynthetic.html'

    def data_set_info_context(self, setname):
        return {"data_info": InjectedContainer.objects.get(title=setname).get_info()}

    @staticmethod
    def get_synthetic_data(request, setname):
        viz = int(request.GET.get("viz", 5))
        injected_data_container = SyntheticDatasetView.load_data_container(setname)

        close = np.isclose(injected_data_container.truth, injected_data_container.injected)
        assert np.allclose(~close == injected_data_container.labels)
        print("assertion passed")
        assert False, "stop here"

        df = injected_data_container.truth
        truth_container = DataContainer(df)
        result = map_truth_data(truth_container, viz)
        cols = [i for i in df.columns]
        injected = injected_data_container.get_none_filled_injected()
        result["injected"] = [map_injected_series(injected[c],cols[i],truth_container) for i,c in enumerate(injected) if i in
                              injected_data_container.injected_columns]
        return JsonResponse(result)
