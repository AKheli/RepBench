from django.urls import path
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from RepBenchWeb.views.recommendation import recommendation_view , file_upload_view
from RepBenchWeb.views import (
    indexview,
    optimizationview,
    dataset_views,
    repair_view,
    injection_view,
)

from RepBenchWeb.views import dimensionality_reduction_view, synthetic_dataset_view, data_loader
app_name = 'RepBenchWeb'

urlpatterns = [
    path('', indexview.index, name='index'),
    path('RepBenchWeb', indexview.index, name='index'),
    path('RepBenchWeb/', indexview.index, name='index'),

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

    path('optimizazionDataSets', optimizationview.OptimizationView().optimization_datasets, name='optimisation_datasets'),

    # alg inspection
    path('alg_inspection', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView.as_view(),
         name="dimensionality_reduction"),
    path('alg_inspection_repair/<str:setname>', dimensionality_reduction_view.DimensionalityReductionView().repair_data,
         name="alg_inspection_repair"),

    # data getter
    path('get_data/<str:setname>', data_loader.get_data, name='get_data'),

    # catch22 sliders getter
    path('sliders_view/<str:setname>', dataset_views.sliders_view, name='get_catch22_data'),


    ## recommendation
    path('recommendation/<str:setname>', recommendation_view.RecommendationView.as_view(), name='recommend'),
    path('recommendation_datasets', recommendation_view.RecommendationView().recommendation_datasets, name='recommendation_datasets'),
    path('get_reccomendation_results/<str:setname>', recommendation_view.RecommendationView.get_recommendation , name="get_recommendation"),


    path('user_recommendation', file_upload_view.upload_files , name="user_recommendation"),
    path('upload/', file_upload_view.upload_files, name='upload_files'),
    # path('user_recommendation', recommendation_view..as_view(), name='user_recommendation'),
]


urlpatterns += [
    # path('RepBenchWeb/', include("RepBenchWeb.urls")),
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='/RepBenchWeb/', permanent=True)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
