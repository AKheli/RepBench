import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from data_methods.data_reader import get_df_from_file


class DataAnalizer:
    def __init__(self,data , name = None):
        if isinstance(data,str):
            self.data , data_name = get_df_from_file(data)
            self.name = data_name if name is None else name
        else:
            self.data = data
        assert isinstance(self.data,pd.DataFrame)

    def plot_data(self):
        self.data.plot()
        plt.show()

    def plot_hist(self):
        self.data.hist()
        plt.show()

    def data_acf(self,lags=10):
        return {name : acf(values,nlags=lags) for name, values in self.data.iteritems()}

    def data_acf_plot(self,lags=100):
        for name, values in self.data.iteritems():
            plot_acf(values, lags=min(len(values), lags))
            plt.title(name)
            plt.show()

    def data_correlation(self):
        return self.data.corr()


    def data_sorted_values(self):
        return pd.DataFrame({name:  sorted(list(enumerate(values)),key= lambda x : abs(x[1]),reverse=True) for name, values in self.data.iteritems()})
