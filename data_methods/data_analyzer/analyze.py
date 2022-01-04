import os

from Repair.Robust_PCA.RPCAestimation.search_param import PCA_paramsearch

os.chdir("../../")  # todo
from data_methods.Helper_methods import get_df_from_file
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf


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


for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
    analyze(file)

# params
import numpy as np
import toml
param_grid = {
    "threshold": np.arange(0.5, 3., 0.2),
    "n_components": [1, 2, 3, 4, 5, 6],
    "delta": [0.5 ** i for i in range(11)],
    "component_method": ["TruncatedSVD"]
}
with open("RPCA_params_bayesian.toml", 'w') as f:
    for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
        print(f"start paramsearch of {file}")
        search = PCA_paramsearch("BAFU.txt", param_grid, ["ba"])
        print(search)
        f.dump(search,f)

with open("RPCA_params.toml", 'w') as f:
    for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
        print(f"start paramsearch of {file}")
        search = PCA_paramsearch("BAFU.txt", param_grid, ["ha"])
        toml.dump(search,f)
