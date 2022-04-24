BASE_SCENARIO = "base"
TS_LENGTH = "ts_len"
ANOMALY_SIZE = "a_size"
ANOMALY_RATE = "a_rate"
ANOMALY_POSITION = "anomaly_position"
ANOMALY_FACTOR  = "anomaly_factor"
TS_NBR ="ts_nbr"
CTS_NBR = "cts_nbr"


default_percentage = 10

scenario_specifications = {
    BASE_SCENARIO: {"anomaly_percentage": default_percentage, "anomaly_size": 1},
    TS_LENGTH: {"anomaly_percentage": default_percentage, "anomaly_size": 1},
    ANOMALY_SIZE: {"anomaly_sizes": [1,2,3,4,5,6,7,8,9,10] , "anomaly_percentage": 3, },
    ANOMALY_RATE: {"anomaly_percentage": 10 , "anomaly_percentages":[0.25,0.5,1,2,4,8,16], "anomaly_size": 1},
    #MINI_SCENARIO: {"length": 25, "anomaly_length": 5},
    ANOMALY_FACTOR: {"anomaly_percentage": 0.10, "anomaly_length": 10},
    TS_NBR : {"anomaly_percentage": 10, "anomaly_size": 1},
    CTS_NBR : {"contaminated_ts": [1,2,3,4,5,6,7,8,9,10]}}
scenario_specifications[ANOMALY_POSITION] = scenario_specifications[BASE_SCENARIO].copy()



SCENARIO_TYPES = list(scenario_specifications.keys())

def parse_scenario_name(type_name):
    type_name = type_name.lower()
    if type_name in SCENARIO_TYPES:
        return type_name
    a_min, v_min = -1, 100
    for scen in SCENARIO_TYPES:
        x = start_of_(type_name, scen)
        if x < v_min:
            a_min, v_min = scen, x
    assert v_min  == 100, f"could not parse scenario {type_name} , must bin in {SCENARIO_TYPES} "
    return a_min


def start_of_(str, type):
    if len(str) == 0:
        return 0
    if len(type) == 0:
        return 100

    if str[0] == type[0]:
        return start_of_(str[1:], type[1:])
    else:
        return start_of_(str, type[1:]) + 1