import TestingFramework as run
import Scenarios.ScenarioConfig as sc
# cts_nbr,ts_nbr,ts_len
import timeit

sc.MAX_N_ROWS  = 20001
start = timeit.timeit()
input = "-scen ts_len -data msd1_5 -rn runtime_len -anom shift -alg all  -t halving -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()

sc.MAX_N_ROWS  = 10001
start = timeit.timeit()
input = "-scen cts_nbr,ts_nbr -data msd1_5 -rn runtime_len -anom shift -alg all  -t halving -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()
