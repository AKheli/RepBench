import json

from django.db import models
import pandas as pd

from injection.injected_data_container import InjectedDataContainer


class DataSet(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=True)
    dataframe = models.JSONField(null=False, blank=False)
    ref_url = models.CharField(max_length=200, null=True, blank=True)
    url_text = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    additional_info = models.JSONField( blank=False)

    # constructor for django database model
    def __str__(self):
        return self.title

    @property
    def df(self):
        return pd.read_json(self.dataframe)


    def get_info(self):
        n, m = self.df.shape
        return {
            "values": n * m,
            "ts_nbr": m,
            "title": self.title,
            "ref_url": self.ref_url,
            "url_text": self.url_text,
            "description": self.description,
        }

    def get_catch_22_features(self):
        additional_info = json.loads(self.additional_info)
        return {"catch22": additional_info["catch22"],
                "catch22_min_max": additional_info["catch22_min_max"]
        }

score_map = { "mae" : "MAE",
                "mse" : "MSE",
                "rmse" : "RMSE",
                "partial_rmse" : "RMSE on Anomaly"
                }

#
# class InjectedContainer(models.Model):
#     title = models.CharField(max_length=64, null=False, blank=False, unique=False)
#     injectedContainer_json = models.JSONField(null=False, blank=False)
#     description = models.TextField(max_length=200, null=True, blank=True)
#

class InjectedContainer(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=False)
    injectedContainer_json = models.JSONField(null=False, blank=False)
    description = models.TextField(max_length=200, null=True, blank=True)
    info = models.JSONField(blank=False,null=True)# orginal data titel


    @property
    def injected_container(self):
        injected_container_ : InjectedDataContainer = InjectedDataContainer.from_json(self.injectedContainer_json)
        return injected_container_

    def get_info(self):
        injectedDataContainer : InjectedDataContainer = self.injected_container
        n, m = injectedDataContainer.injected.shape
        a_rates = injectedDataContainer.get_a_rate_per_col()
        scores = injectedDataContainer.original_scores
        scores = {  score_map[k] : round(v,4) for k,v in scores.items() if k in score_map.keys() }
        return {
            "values": n * m,
            "ts_nbr": m,
            "title": self.title,
            "description": self.description,
            "anomaly_rates": a_rates,
            "injected_rates": {ts:r for ts,r in a_rates.items() if r >0},
            "scores": scores
        }

    def __str__(self):
        return self.title
