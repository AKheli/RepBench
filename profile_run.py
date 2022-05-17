import TestingFramework as run

input = " -scen all -data airqualityuci -anom all -alg cdrec,subcdrec" # "-scen vary_ts_length  -col 0  -data YAHOO.csv -anom a -algo 1 "

run.main(input)