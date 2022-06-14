import TestingFramework as run

import timeit
start = timeit.timeit()
input = "-scen all -data all -rn mae_b -anom all -alg all  -t bayesian -e mae"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
end = timeit.timeit()
print(end-start)
start = timeit.timeit()