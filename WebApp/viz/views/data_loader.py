from django.http import JsonResponse

from Injection.injected_data_container import InjectedDataContainer
from WebApp.viz.models import DataSet, InjectedContainer
from WebApp.viz.ts_manager.HighchartsMapper import map_truth_data, map_injected_series
from data_methods.data_class import DataContainer


def load_data_container(setname,viz=4):
    if DataSet.objects.filter(title=setname).exists():
        df = DataSet.objects.get(title=setname).df
        return DataContainer(df)
    try:
        injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container
    except InjectedContainer.DoesNotExist:
        raise ValueError(f"No dataset with name: {setname} found {InjectedContainer.objects.all()}")
    return DataContainer(injected_data_container.injected)


def get_data(request, setname,viz=4):
    viz = int(request.GET.get("viz", viz))
    if DataSet.objects.filter(title=setname).exists():
        df = DataSet.objects.get(title=setname).df
        return JsonResponse(map_truth_data(DataContainer(df), viz))

    injected_data_container: InjectedDataContainer = InjectedContainer.objects.get(title=setname).injected_container
    df = injected_data_container.truth
    truth_container = DataContainer(df)
    result = map_truth_data(truth_container, viz)
    cols = [i for i in df.columns]
    injected = injected_data_container.get_none_filled_injected()
    result["injected"] = [map_injected_series(injected[c], cols[i], truth_container) for i, c in enumerate(injected) if
                          i in
                          injected_data_container.injected_columns]
    return JsonResponse(result)
