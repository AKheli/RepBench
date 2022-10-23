from django.urls import path
from web.mysite.viz.views import indexview,optimizationview

urlpatterns = [
    path('', indexview.index, name='index'),
    path('get_data', indexview.get_data, name='get_data'),
    path('get_data/<str:dataset>', indexview.get_data, name='get_data'),

    path('inject/<str:dataset>', indexview.inject, name='inject'),
    path('repair/<str:dataset>', indexview.repair, name='repair'),
    path('opt' , optimizationview.optimization_view , name="optimization"),

    path('display_dataset', indexview.display_datasets, name='display_dataset'),
    path('viz_dataset/<str:setname>', indexview.viz_dataset, name='viz_dataset'),
    path('<str:setname>', indexview.index, name='index'),


    path('optimize/<str:dataset>', optimizationview.optimize, name='optimize'),




]
