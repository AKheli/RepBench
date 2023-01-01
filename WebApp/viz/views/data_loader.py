import numpy as np
from django.http import JsonResponse

from Injection.injected_data_container import InjectedDataContainer
from WebApp.viz.models import DataSet, InjectedContainer
from WebApp.viz.ts_manager.HighchartsMapper import map_truth_data, map_injected_data_container
from data_methods.data_class import DataContainer


def load_data_container(setname,viz=4):
    if DataSet.objects.filter(title=setname).exists():
        data_object = DataSet.objects.get(title=setname)
        df = data_object.df
        title = data_object.title
        return DataContainer(df, title=title)
    try:
        injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container
    except InjectedContainer.DoesNotExist:
        raise ValueError(f"No dataset with name: {setname} found {InjectedContainer.objects.all()}")
    return DataContainer(injected_data_container.truth)


def get_data(request, setname,viz=4):
    viz = int(request.GET.get("viz", viz))
    if DataSet.objects.filter(title=setname).exists():
        df = DataSet.objects.get(title=setname).df
        return JsonResponse(map_truth_data(df,viz=viz))

    injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container

    close = np.isclose(injected_data_container.truth.values, injected_data_container.injected.values)
    assert np.allclose(~close, injected_data_container.class_df.values)
    results = map_injected_data_container(injected_data_container)
    return JsonResponse(results)
