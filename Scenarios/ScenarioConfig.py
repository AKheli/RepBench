BASE_SCENARIO = "base"
TS_LENGTH = "ts_len"
ANOMALY_SIZE = "a_size"
ANOMALY_RATE = "a_rate"
ANOMALY_POSITION = "anomaly_position"
ANOMALY_FACTOR  = "anomaly_factor"
TS_NBR ="ts_nbr"
CTS_NBR = "cts_nbr"


default_percentage = 5
default_length = 10

scenario_specifications = {
    BASE_SCENARIO: {"a_percentage": default_percentage, "a_length": default_length},
    TS_LENGTH: {"a_percentage": default_percentage, "a_length": default_length},
    ANOMALY_SIZE: {"a_lengths": [5,10,20,30,50,100] , "a_percentage": default_percentage/2 },
    ANOMALY_RATE: {"a_percentages":[0.25,0.5,1,2,5,10], "a_length": default_length},
    TS_NBR : {"a_percentage": default_percentage,"a_length" : default_length },
    CTS_NBR : {"contaminated_ts": [1,2,3,4,5,6,7,8,9,10],"a_percentage" : default_percentage/2}
}
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