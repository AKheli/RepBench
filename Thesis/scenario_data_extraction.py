import pandas
import pandas as pd
from matplotlib import pyplot as plt


"""
humidity distortion length 300, -1
bafu 
msd outliers a_rate 10,2500
"""
from Injection.Scenarios.scen_gen import build_scenario
import numpy as np
scen_name  ="a_rate"
file_name = "elec"
scenario  = build_scenario(scen_name, file_name, "test", "outlier", cols = [0])


dfs = []
start,stop = 200 , 400
for name, injected_container in scenario.name_container_iter:
    injected,truth = injected_container.injected.iloc[start:stop,:] , injected_container.truth.iloc[start:stop,:]
    anoms = np.invert(np.isclose(truth.values,injected.values))

    extended = np.zeros_like(anoms)
    for i,col in enumerate(anoms.T):
        extended[:,i] = np.convolve(col,[True,True,True],"same")

    inj_cols = injected_container.injected_columns
    # plt.plot(extended[:,injected_container.injected_columns])
    # plt.plot(anoms[:,injected_container.injected_columns].astype(int)+1)
    # plt.plot(extended[:,injected_container.injected_columns]-anoms[:,injected_container.injected_columns].astype(int))
    # plt.show()
    inv_f = lambda df :  scenario.data_container.inf_norm_f(df)
    injected , truth = inv_f(injected) , inv_f(truth)
    injected.iloc[np.invert(extended)] = np.nan
    plt.plot(truth.iloc[:, inj_cols])
    plt.plot(injected.iloc[:, inj_cols] , color="red")
    data = injected.iloc[:, inj_cols].values.ravel()
    plt.title( np.count_nonzero(~np.isnan(data))/len(data))
    plt.show()
    df = pd.DataFrame(np.array([truth.iloc[:, inj_cols].values.ravel(), injected.iloc[:, inj_cols].values.ravel()]).T, columns=[f"truth{name}",f"injected{name}"])
    dfs.append(df)

df = pandas.concat(dfs,axis=1)
df.index.name = 't'
df.to_csv(f"{scen_name}.txt",na_rep='nan')