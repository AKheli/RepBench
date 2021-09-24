from tsag import PointAnomaly
import numpy as np
import pandas as pd
n = 10
timeseries =  pd.Series(np.arange(1000),np.ones(1000))
template = timeseries[:n]
# Generate point anomaly
point_anomaly = PointAnomaly(template)
point_anomaly.plot()

# Insert generated anomaly into time series data
augmented_timeseries = point_anomaly.insert(timeseries, index=None)

#pd.plot(timeseries)