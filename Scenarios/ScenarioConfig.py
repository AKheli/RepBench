BASE_SCENARIO = "base"
TS_LENGTH = "ts_len"
ANOMALY_SIZE = "a_size"
ANOMALY_RATE = "a_rate"
ANOMALY_POSITION = "anomaly_position"
ANOMALY_FACTOR  = "anomaly_factor"
TS_NBR ="ts_nbr"
CTS_NBR = "cts_nbr"

MAX_N_ROWS = 1500000
MAX_N_COLS = 10000

default_percentage = 5
default_length = 10

scenario_specifications = {
    BASE_SCENARIO: {"a_percentage": default_percentage, "a_length": default_length},
    TS_LENGTH: {"a_percentage": default_percentage, "a_length": default_length,"length_percentages": [30,40,50,60,70,80,90,100]},
    ANOMALY_SIZE: {"a_percentage": default_percentage/2, "a_lengths": [5,10,20,40,60,80,100,200]  },
    ANOMALY_RATE: {"a_percentages":[0.25,0.5,1,2,5,10,15,20], "a_length": default_length},
    TS_NBR : {"a_percentage": default_percentage,"a_length" : default_length , "ts_nbrs": [3,4,5,6,7,8,9,10]},
    CTS_NBR : {"a_percentage" : default_percentage ,"a_length": default_length ,"cts_nbrs": [1,2,3,4,5,6,7,8,9,10]}
}
scenario_specifications[ANOMALY_POSITION] = scenario_specifications[BASE_SCENARIO].copy()


SCENARIO_TYPES = list(scenario_specifications.keys())
