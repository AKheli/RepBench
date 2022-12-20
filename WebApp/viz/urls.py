from django.urls import path

from WebApp.viz.views import (
    indexview,
    optimizationview,
    dataset_views,
    repair_view,
    dimensionality_reduction_view,
    synthetic_dataset_view,
    data_loader,
    injection_view,
)

urlpatterns = [
    path('', indexview.index, name='index'),

    path('display_datasets', dataset_views.display_datasets, name='display_datasets'),


    path('display_dataset/<str:setname>', dataset_views.DatasetView.as_view(), name='display_dataset'),
    path('display_dataset_synthetic/<str:setname>', synthetic_dataset_view.SyntheticDatasetView.as_view(),
         name='synthetic_dataset_view'),

    path('repairDatasets', repair_view.RepairView.repair_datasets, name='repair_datasets'),
    path('repairDataset/<str:type>', repair_view.RepairView.repair_datasets, name='repair_datasets'),

    ## repair view
    path('repair', repair_view.RepairView.as_view(), name='repair'),
    path('repair/<str:setname>', repair_view.RepairView.as_view(), name='repair'),

    path('injection/<str:setname>', injection_view.InjectionView.as_view(), name='injection'),


    # store and inject data
    path('inject_data/<str:setname>', injection_view.inject_data, name='inject_data'),
    path('store_data/<str:setname>', injection_view.store_data, name='store_data'),

    ##  repair data
    path('repair_data/<str:setname>', repair_view.RepairView.repair_data, name='repair_data'),

    # optimization
    path('opt', optimizationview.OptimizationView.as_view(), name="opt"),
    path('opt/<str:setname>', optimizationview.OptimizationView.as_view(), name="opt"),
    path('optimize_data/<str:setname>', optimizationview.OptimizationView.optimize, name='optimize_data'),
    path('fetch_optresults', optimizationview.fetch_opt_results, name='fetch_optresults'),


    # alg inspection
    path('alg_inspection', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection_repair/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView().repair_data,
         name="alg_inspection_repair"),

    # data getter
    path('get_data/<str:setname>', data_loader.get_data, name='get_data'),
]
