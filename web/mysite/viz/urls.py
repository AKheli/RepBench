from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_data', views.get_data, name='get_data'),
    path('get_data/<str:dataset>', views.get_data, name='get_data'),

    path('inject/<str:dataset>', views.inject, name='inject'),
    path('repair/<str:dataset>', views.repair, name='repair'),
    path('optim', views.optim, name='optim'),
    path('display_dataset', views.display_datasets, name='display_dataset'),
    path('viz_dataset/<str:setname>', views.viz_dataset, name='viz_dataset'),
    path('<str:setname>', views.index, name='index'),

]
