from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from pandas import DataFrame

from web.mysite.viz.forms.injection_form import UserForm



def get_data(request):
    data_set = request.POST.get("dataset","bafu5k")
    df: DataFrame = pd.read_csv(f"../../data/train/{data_set}.csv")
    data = {
        'series': [{"visible": i < 5, "id": str(i), "name": col_name, "data": list(df[col_name])} for (i, col_name) in
                   enumerate(df.columns)]}
    data["series"][2]["linkedTo"] = str(0)
    data["series"][2]["color"] = "red"

    data["series"][1]["linkedTo"] = str(0)
    data["series"][1]["color"] = "red"
    return JsonResponse(data)

def index(request):
    a = request
    """ view function for sales app """
    if request.POST.get("type",None) == "injection":
        print("JSSSSOOOON RESPONSE")
        df : DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
        data = {'series': [{"name": col_name, "data": list(df[col_name])} for col_name in df.columns]}
        return JsonResponse(data)

    elif request.POST.get("type", None) == "load_data_set":
        df: DataFrame = pd.read_csv("../../data/train/bafu5k.csv")
        data = {'series': [{ "visible": i < 5,  "id" : str(i),"name": col_name, "data": list(df[col_name]) } for (i, col_name) in enumerate(df.columns)]}
        data["series"][2]["linkedTo"] = str(0)
        data["series"][2]["color"] = "red"

        data["series"][1]["linkedTo"] = str(0)
        data["series"][1]["color"] = "red"
        return JsonResponse(data)
    else:

        df : DataFrame = pd.read_csv("../../data/train/humidity.csv")
        table_content = df.to_html(index=None)
        context = {"table_data" : [] , 'series' : [ {"name" : col_name , "data" :  list(df[col_name])}  for col_name in df.columns]}

        form = UserForm()
        context["form"] = form
    return render(request, 'index.html', context=context)

