import os

from ParameterTuning.search_param import PCA_paramsearch
from Repair.Screen.SCREEN_repair import SCREEN_estimator

os.chdir("../../")  # todo
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


# for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
#     analyze(file)
#
# # params

#
# param_grid = {
#     "threshold": np.arange(0.5, 3., 0.2),
#     "n_components": [1, 2, 3, 4, 5, 6],
#     "delta": [0.5 ** i for i in range(11)],
#     "component_method": ["TruncatedSVD"]
# }
#
#
# for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
#     with open(f"{file}_RPCA_params_bayesian.toml", 'w+') as f:
#         print(f"start paramsearch of {file}")
#         search = PCA_paramsearch(file, param_grid, ["ba"] ,Robust_PCA_estimator(cols=[0,1]))
#         print(search)
#         toml.dump(search, f)

# with open("RPCA_params.toml", 'w') as f:
#     for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
#         print(f"start paramsearch of {file}")
#         search = PCA_paramsearch(file, param_grid, ["gr"],Robust_PCA_estimator(cols=[0,1]))
#         toml.dump(search, f)

#screen
param_grid = {
    "T": (1,2000),
    "s": [1, 2, 3, 4, 5, 6],
}
with open("SCREEN bayesia.toml", 'w') as f:
    for file in [x for x in os.listdir("Data") if not os.path.isdir(f"Data/{x}")]:
        print(f"start paramsearch of {file}")
        search = \
            PCA_paramsearch(file, param_grid, ["ba"],SCREEN_estimator(cols=[0,1]))
        toml.dump(search, f)
