BASE_SCENARIO = "base_scenario"
VARY_TS_LENGHT = "vary_ts_lenght"
VARY_ANOMALY_SIZE = "vary_anomaly_size"
VARY_ANOMALY_AMOUNT = "vary_anomaly_amount"

scenario_specifications = {
    BASE_SCENARIO: {"anomaly_percentage": 0.15, "anomaly_length": 15},
    VARY_TS_LENGHT: {"anomaly_percentage": 0.15, "anomaly_length": 15},
    VARY_ANOMALY_SIZE: {"anomaly_length_start": 10, "anomaly_length_step": 10},
    VARY_ANOMALY_AMOUNT: {"anomaly_percentage": 0.15, "anomaly_length": 15}
}

SCENARIO_TYPES = scenario_specifications.keys()






def parse_scenario_name(type_name):
    type_name = type_name.lower()
    if type_name in SCENARIO_TYPES:
        return type_name
    a_min, v_min = -1, 100
    for anom in SCENARIO_TYPES:
        x = start_of_(type_name, anom)
        if x < v_min:
            a_min, v_min = anom, x
    assert v_min < 100, "could not parse scenario"
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