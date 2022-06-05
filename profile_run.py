import TestingFramework as run


input = " -scen all -data humidity -rn full_rmse -anom all -alg all  -t bayesian -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)



# input = " -scen a_rate -data all -rn full_rmse -anom all -alg all  -t bayesian -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#
# input = " -scen a_rate -data all -rn mae -anom all -alg all  -t bayesian -e mae"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#
# input = " -scen cts_nbr -data all -rn partial_rmse -anom all -alg all  -t bayesian -e partial_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)