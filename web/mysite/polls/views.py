from django.shortcuts import render
from django.http import HttpResponse


from Injection.injection_config import label_rate
def index(request,**kwargs):
    model = kwargs['model']
    print(model)
    return HttpResponse(f"Hello, {label_rate} world. You're at the polls index.")