import TestingFramework as run
import Scenarios.ScenarioConfig as scen_config
# cts_nbr,ts_nbr,ts_len
import timeit
from Scenarios.data_part import DataPart
import os


# scen_config.MAX_N_COLS = 10
# run.main(input)

input = "-scen a_rate -data bafu  -rn test -anom shift -alg screen,imr  -e full_rmse  "  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
scen_config.MAX_N_COLS = 10
run.main(input)


# scen_config.labelrate = 0.2
# scen_config.anomstartlabelrate = 0.5
# input = " -alg imr,rpca -data all -a_type shift -scen ts_len -rn imrcomp1"
# run.main(input)
#
# scen_config.labelrate = 0.2
# scen_config.anomstartlabelrate = 0.2
# input = " -alg imr,rpca -data all -a_type shift -scen ts_len -rn imrcomp2"
# run.main(input)
#
# scen_config.label_rate = 0.1
# scen_config.anomstartlabelrate = 0.1
# input = " -alg imr,rpca -data all -a_type shift -scen ts_len -rn imrcomp3"

# input = "-scen  cts_nbr -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#![](Results/col3/ts_len/outlier/bafu5k/precision/error/partial_mutual_info/partial_mutual_info.png)
# input = "-scen  ts_nbr  -data elec,msd1_5 -rn run_time -anom shift -alg all -e full_rmse  -rtn 10"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)
#


# sc.MAX_N_ROWS  = 1000
# input = "-scen all -data humidity -rn default -anom shift -alg all -e full_rmse"  # algox" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "
# run.main(input)



