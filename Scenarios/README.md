# Description of recovery scenarios


## Setup
- The first half of the Time series are used for training 
and the second half for testing .
- when percentage or division is mentioned, the result is floored down to nearest integer.
- The anomalies are placed randomly with 5% of the series space at the start , the end and between the anomalies.
- 
## Scenarios
N = lentgh of time series 
M = number of time series

W = 10% * N

base:
- N = max; M = max;
- The first time series is injected with ~10% anomalies each anomaly has length 20.
- **Is used for training in all scenarios.**

ts_length:
- M = max; N varies between 20% and 100% of the series;
- The first time series is injected with ~10% anomalies each anomaly has length 20.

ts_nbr*:
- N = max; M = varies from 3 columns to 100% of columns;
- The first time series is injected with ~10% anomalies each anomaly has length 20.

miss_disj:
- N = max; M = max;
- Missing data - size = N/M, position: in each time series = column_index * size

miss_over:
- N = max; M = max;
- Missing data - size = 2 * N/M for all columns except last; last column = N/M; position: in each time series = column_index * (size/2)

mcar\*:
- N = max; M = max;
- Missing data - 10 to 100% time series are incomplete; Missing blocks - size = 10, removed from a random series at a random position until a total of W of all points of time series are missing.

blackout:
- N = max; M = max;
- Missing data - 10 to 100 rows in each time series, position: at 5% of all series from the top.

\* ts_nbr is the only scenario that modifies the train set by only selecting the time series that are used for testing
