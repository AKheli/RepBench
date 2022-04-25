import run as run
input = " -scen a_rate -data bafu5k,msd -anom shift,outlier -alg cdrec,rpca" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "

run.main(input)