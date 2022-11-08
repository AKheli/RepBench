import TestingFramework as run
import Injection.injection_config as ic

ic.MAX_N_ROWS = 10000

import matplotlib
matplotlib.use('TKAgg')

# input = "-scen  cts_nbr  -data all  -rn cts_nbr_f2 -anom shift,outlier -alg all -e full_rmse" # "
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)


input = "-scen  a_rate,a_factor  -data elec  -rn all_ts_cont -anom shift,outlier -alg all -ts all" # "
ic.MAX_N_COLS = 10
ic.label_seed = 20
run.main(input)

# input = "-scen  cts_nbr,a_factor  -data all  -rn screen_test2 -anom shift,outlier -alg screen -ts all" # "
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)


# input = "-scen  a_rate,a_factor  -data humidity  -rn single_contaminated_check -anom shift,outlier -alg all -e full_rmse" #
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)
#
# input = "-scen  a_factor,a_rate  -data all  -rn all_ts_cont -anom outlier,shift -alg all -e full_rmse -ts all "
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)


# input = "-scen  a_factor,a_rate  -data all  -rn full_contaminated -anom outlier,shift -alg all -e full_rmse -ts all"
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)

# input = "-scen  cts_nbr  -data all  -rn ctss_nbrs_again2 -anom outlier,shift -alg all -e full_rmse"
# ic.MAX_N_COLS = 10
# ic.label_seed = 20
# run.main(input)




