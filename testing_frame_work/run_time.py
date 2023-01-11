import TestingFramework as run
import injection.injection_config as sc
# cts_nbr,ts_nbr,ts_len
import timeit

import matplotlib
matplotlib.use('TKAgg')

sc.MAX_N_ROWS  = 200000
start = timeit.timeit()
input = "-scen ts_len -data all -rn runtime  -anom shift -alg all -e full_rmse -rtn 20"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()

sc.MAX_N_ROWS = 10000
sc.MAX_N_COLS = 20

start = timeit.timeit()
input = "-scen ts_nbr,cts_nbr -data all -rn runtime -anom shift -alg all -e full_rmse -rtn 20"
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()

