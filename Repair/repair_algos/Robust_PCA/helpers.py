import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale


def normalized_anomaly_scores(df_original, df_reconstructed , axis = 0):
    diff = np.sum((np.array(df_original) - np.array(df_reconstructed)) ** 2, axis=axis)
    diff = pd.Series(data=diff, index=df_original.index)
    return minmax_scale(diff)
