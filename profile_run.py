import TestingFramework as run

import timeit
start = timeit.timeit()
input = "-scen cts_nbr -data msd1_5 -rn runtime -anom shift -alg all  -t bayesian -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()