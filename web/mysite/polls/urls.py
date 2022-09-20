from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index',kwargs={"model" : 100000}),
]