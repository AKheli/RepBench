from django.urls import path

import web.mysite.viz.views.dataset_views
from web.mysite.viz.views import indexview,optimizationview,dataset_views

urlpatterns = [
    path('inject/<str:dataset>', indexview.inject, name='inject'),
    path('repair/<str:dataset>', indexview.repair, name='repair'),

    # optimization
    path('opt' , optimizationview.optimization_view , name="optimization"),
    path('optimize/<str:dataset>', optimizationview.optimize, name='optimize'),



    # dataset
    path('viz_dataset/<str:setname>', web.mysite.viz.views.dataset_views.viz_dataset, name='display_dataset'),
    path('display_datasets', web.mysite.viz.views.dataset_views.display_datasets, name='display_datasets'),


    path('get_data/<str:dataset>', dataset_views.get_data, name='get_data'),


    path('', indexview.index, name='index'),
    path('<str:setname>', indexview.index, name='index'),

]
