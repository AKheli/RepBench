import os


from data_methods.Helper_methods import get_df_from_file
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

import toml

def analyze(data_name, optim_params=False, anomaly_types=[], path="data_methods/data_analyzer"):
    df, name = get_df_from_file(data_name)
    path = f'{path}/{name}'

    if not os.path.exists(path):
        os.mkdir(path)

    df.plot()
    plt.savefig(f"{path}/data.svg")

    df.hist()
    plt.savefig(f"{path}/hist.svg")

    acr = df.iloc[:, 0].autocorr(lag=10)
    plot_acf(df.iloc[:, 0], lags=min(len(df.iloc[:, 0]) - 10, 1000))
    plt.savefig(f"{path}/acf.svg")



