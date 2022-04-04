# Description of recovery scenarios


## Setup
- The first half of the Time series are used for training 
and the second half for testing .

[comment]: <> (- when percentage or division is mentioned, the result is floored down to nearest integer.)
- The anomalies are placed randomly with 5% of the series space at the start , the end and between the anomalies.

## Scenarios
N = length of time series 
M = number of time series

K = 1% of N
base:
- N = max; M = max;
- The first time series is injected with ~10% anomalies each anomaly has length max(10,K).
- **Is used for training in all scenarios.**

ts_length:
- M = max; N varies between 20% and 100% of the series;
- The first time series is injected with ~10% anomalies each anomaly has length max(10,1% of max).

ts_nbr*:
- N = max; M  varies from 3 columns to 100% of the columns;
- The first time series is injected with ~10% anomalies each anomaly has length max(10,K).

anomaly_length: (maybe multiple anomalies but this really depends on the data size)
- N = max; M = max;
- The first time series is injected with 1 anomaly and the size is increased from max(10,K) to 30% of the time series

anomaly_factor:
- N = max; M = max;
- The first time series is injected with ~10% anomalies each anomaly has length max(10,K).
- The difference of the anomalous points is changed from 1/4 to 4 time the normal level.

-infected_ts_nbr
- N = max; M = max
- number of infected time series from 1 to M  each containing ~10% anomalies each anomaly has length 20 placed randomly

-all_infected_length 
- N = max; M = max
- All time series are injected with 1 anomaly, the size is increased from max(10,K) to  30% of the time series placed randomly.

-blackout_length
- N = max; M = max
- All time series are injected with 1 anomaly,  the size is increased from max(10,K ) to 30% of the time series starting at 20% of the time series.


\* ts_nbr is the only scenario that modifies the train set by only selecting the time series that are used for training
