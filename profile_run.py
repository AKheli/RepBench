import TestingFramework as run

input = " -scen all -data all -rn mae -anom shift -alg all  -t bayesian -e mae"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)

# input = " -scen a_rate -data humidity -rn test -anom shift -alg imr,screen  -t bayesian -e partial_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
