# Description of anomaly repair scenarios


## Setup
- The first half of the time series are used for training 
and the second half for testing.
- We place anomalies randomly after the first 5% of the time series to not start inside an anomaly and the anomalies do not overlap.
- Specifications of lengths exclude point outliers.


## Scenarios
N = length of time series 
M = number of time series

K = 1% of N


base:
- N = max; M = max;
- The first time series is contaminated with ~10% anomalies each anomaly has length max(10,K).
- **Is used for training in all scenarios.**

ts_length:
- M = max; N varies between 30% and 100% of the series growing equally at the start and the end, since more information on both sides might give a better repair.
- The first time series is contaminated with ~5% of N max anomalies each anomaly has length max(10,1% of N max) and only the initial 30% of the time series are contaminated.

a_length: 
- N = max; M = max;
- The first time series is contaminated with 3 anomalies and the size is increased from K to 10% of the time series.

a_rate:
- N = max; M = max;
- The first time series is contaminated with 1 to 30 anomalies each anomaly has length K.

a_dtype:
- N = max; M = max;
- Successively adds different anomaly types into the first time series the order is specified by -a. The total contamination rate is always ~10%
- If -a = all, the order is: point_outlier , shift , distortion , growth change. This means we start with a time series only containing point outliers then a time series containing point outliers and shifts. The next time series contains point outliers, shifts and distortions and the last one all anomaly types.

a_rtype: 
- N = max; M = max;
- The first time series is contaminated with ~10% anomalies each anomaly has length max(10,1% of N max).
- As in a_dtype but the order in which the anomalies are added is random.

ts_nbr:
- N = max; M  varies from 3 columns to 100% of the columns;
- The first time series is contaminated with 10 anomalies each anomaly has length K.

cts_nbr:
- N = max; M = max
- Number of infected time series from 1 to M  each containing 10 anomalies. Each anomaly has length K and is placed randomly.





