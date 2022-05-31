import TestingFramework as run


input = " -scen a_rate,a_size -data all -rn full_rmse -anom all -alg all  -t bayesian -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
