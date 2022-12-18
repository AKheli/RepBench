
from django.shortcuts import render

def index(request, setname="bafu5k"):
    context = {}
    return render(request, 'index.html', context=context)

