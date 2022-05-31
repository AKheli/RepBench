import TestingFramework as run

# input = " -scen a_size -data humidity -rn testpart -anom outlier -alg cdrec  -t bayesian -e partial_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)

input = " -scen a_size -data bafu5k,humidity -rn testfull -anom  outlier -alg imr,cdrec  -t bayesian -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)

input = " -scen a_size -data bafu5k,humidity -rn testpartial -anom  outlier -alg imr,cdrec  -t bayesian -e partial_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)
" -scen all -data all -rn partial_rmse -anom shift -alg all  -t bayesian -e partial_rmse"