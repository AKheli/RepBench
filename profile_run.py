import TestingFramework as run
import Scenarios.ScenarioConfig as scen_config
# cts_nbr,ts_nbr,ts_len
import timeit
from Scenarios.data_part import DataPart
import os


# scen_config.MAX_N_COLS = 10
# input = "-scen  ts_nbr -data elec,msd1_5 -rn withparams -anom shift -alg screen,rpca,cdrec,imr -e full_rmse  "  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)

scen_config.MAX_N_COLS = 10
input = "-scen  ts_len -data all -rn tslentst -anom all -alg screen,rpca,imr "  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
input = " -alg screen,screenglobal -data bafu -a_type all -scen a_size"
run.main(input)

# input = "-scen  cts_nbr -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#![](Results/col3/ts_len/outlier/bafu5k/precision/error/partial_mutual_info/partial_mutual_info.png)
# input = "-scen  ts_nbr  -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse  -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#


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
