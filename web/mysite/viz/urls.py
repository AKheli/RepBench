from django.urls import path

import web.mysite.viz.views.dataset_views
from web.mysite.viz.views import indexview,optimizationview,dataset_views,repair_view,alg_inspection_view

urlpatterns = [
    path('', indexview.index, name='index'),
    path('display_datasets', web.mysite.viz.views.dataset_views.display_datasets, name='display_datasets'),
    path('display_dataset/<str:setname>', dataset_views.DatasetView.as_view(), name='display_dataset'),

    ## repair view
    path('repair', repair_view.RepairView.as_view(), name='repair'),
    path('repair/<str:setname>', repair_view.RepairView.as_view(), name='repair'),

    ## fetch and get repair
    path('repair_data/<str:setname>', repair_view.RepairView.repair_data, name='repair_data'),
    path('inject_data/<str:setname>', repair_view.RepairView.inject_data, name='inject_data'),


    # optimization
    path('opt', optimizationview.OptimizationView.as_view(), name="opt"),
    path('opt/<str:setname>' , optimizationview.OptimizationView.as_view() , name="opt"),
    path('optimize_data/<str:setname>', optimizationview.OptimizationView.optimize, name='optimize_data'),


    # alg inspection
    path('alg_inspection', alg_inspection_view.AlgInspectionView.as_view(), name="alg_inspection"),
    path('alg_inspection_repair/<str:setname>' , alg_inspection_view.AlgInspectionView().repair_data , name="alg_inspection_repair"),

    # datagetter
    path('get_data/<str:setname>', dataset_views.DatasetView().get_data, name='get_data'),
]
