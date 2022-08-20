import TestingFramework as run
import Scenarios.ScenarioConfig as scen_config
# cts_nbr,ts_nbr,ts_len
import timeit

scen_config.MAX_N_COLS = 10
input = "-scen  all -data elec,msd1_5 -rn test -anom shift -alg screen -e full_rmse  "  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)

input = "-scen  cts_nbr -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)

input = "-scen  ts_nbr  -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse  -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
run.main(input)



# sc.MAX_N_ROWS  = 1000
# input = "-scen all -data humidity -rn default -anom shift -alg all -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)



# sc.MAX_N_ROWS  = 10001
# start = timeit.timeit()
# input = "-scen cts_nbr,ts_nbr -data msd1_5 -rn runtime_len -anom shift -alg all  -t halving -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
# end = timeit.timeit()
# print(end-start)
# start = timeit.timeit()
