from django.db import models
import pandas as pd

from Injection.injected_data_part import InjectedDataContainer


class DataSet(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=True)
    dataframe = models.JSONField(null=False, blank=False)
    ref_url = models.CharField(max_length=200, null=True, blank=True)
    url_text = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

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
            "description": self.description
        }


# class InjectedDataSet(models.Model):
#     title = models.CharField(max_length=64, null=False, blank=False, unique=False)
#     original_series_id = models.ForeignKey(DataSet, on_delete=models.CASCADE)
#     injectedDataframe = models.JSONField(null=False, blank=False)
#     description = models.TextField(max_length=200, null=True, blank=True)
#
#     @property
#     def df(self):
#         return pd.read_json(self.injectedDataframe)
#
#     def original_df(self):
#         return self.original_series_id.df
#
#     def get_info(self):
#         n, m = self.df.shape
#         return {
#             "values": n * m,
#             "ts_nbr": m,
#             "title": self.title,
#             "description": self.description
#         }


class InjectedContainer(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=False)
    injectedContainer_json = models.JSONField(null=False, blank=False)
    description = models.TextField(max_length=200, null=True, blank=True)

    @property
    def injected_container(self):
        injected_container_ : InjectedDataContainer = InjectedDataContainer.from_json(self.injectedContainer_json)
        return injected_container_

    def get_info(self):
        n, m = self.injected_container.injected.shape
        return {
            "values": n * m,
            "ts_nbr": m,
            "title": self.title,
            "description": self.description
        }

    def __str__(self):
        return self.title
