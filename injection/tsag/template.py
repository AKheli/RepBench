from tsag.tsag import PointAnomaly
import numpy as np
import pandas as pd
from tsag import FrequencyShiftAnomaly, AmplitudeShiftAnomaly, RangeShiftAnomaly, CompoundAnomaly

n = 10
timeseries =  np.sin(np.arange(20))
template = timeseries[:n].copy()

args = [
    # [Generator, {Arguments}],
    [FrequencyShiftAnomaly, {'ratio':1 }],
    [AmplitudeShiftAnomaly, {'ratio': 0}],
    [RangeShiftAnomaly, {'ratio': 0.5}],
]

# Generate compound anomaly
compound_anomaly = CompoundAnomaly(template, *args)
compound_anomaly.plot()

# Insert generated anomaly into time series data
augmented_timeseries = compound_anomaly.insert(template, index=None)