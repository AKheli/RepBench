##### Anomalies
AMPLITUDE_SHIFT = "shift"
DISTORTION = "distortion"
GROWTH_CHANGE = "growth"
POINT_OUTLIER = "outlier"

ANOMALY_TYPES = (AMPLITUDE_SHIFT,
                 DISTORTION,
                 GROWTH_CHANGE,
                 POINT_OUTLIER)

BASE_FACTORS = {AMPLITUDE_SHIFT: 2,
                DISTORTION: 2,
                POINT_OUTLIER: 2}

DEFAULT_PERCENTAGE = 5
DEFAULT_LENGTH = 30  # ignored by pointoutliers

BASE_ANOMALY_SETTINGS = {"a_percentage": DEFAULT_PERCENTAGE,
                         "a_length": DEFAULT_LENGTH}

##### Scenarios
BASE_SCENARIO = "base"
TS_LENGTH = "ts_len"
ANOMALY_SIZE = "a_size"
ANOMALY_RATE = "a_rate"
#ANOMALY_POSITION = "a_position"
ANOMALY_FACTOR = "a_factor"
TS_NBR = "ts_nbr"
CTS_NBR = "cts_nbr"


MAX_N_ROWS = 20000
MAX_N_COLS = 10

scenario_specifications = {
    BASE_SCENARIO: BASE_ANOMALY_SETTINGS,
    TS_LENGTH: {"a_percentage": DEFAULT_PERCENTAGE * 2, "a_length": DEFAULT_LENGTH,
                "length_ratio": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]},
    ANOMALY_SIZE: {"a_percentage": DEFAULT_PERCENTAGE / 2, "a_length": [5, 10, 20, 40, 60, 80, 100, 200]},
    ANOMALY_RATE: {"a_percentage": [0.0025, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15, 0.2], "a_length": DEFAULT_LENGTH},
    TS_NBR: {"a_percentage": DEFAULT_PERCENTAGE, "a_length": DEFAULT_LENGTH, "ts_nbr": [3, 4, 5, 6, 7, 8, 9, 10]},
    CTS_NBR: {"a_percentage": DEFAULT_PERCENTAGE, "a_length": DEFAULT_LENGTH,
              "cts_nbr": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    ANOMALY_FACTOR : { "a_factors" : [0.5,1,2,3,4,5,10,20], "a_length": DEFAULT_LENGTH , "a_percentage": DEFAULT_PERCENTAGE}
}

SCENARIO_TYPES = list(scenario_specifications.keys())

### imr labels
label_seed = 100
label_rate = 0.2
anomstartlabelrate = 0.2


def parse_anomaly_name(type_name):
    type_name = type_name.lower()
    if type_name in ANOMALY_TYPES:
        return type_name
    a_min, v_min = -1, 100
    for anom in ANOMALY_TYPES:
        x = start_of_(type_name, anom)
        if x < v_min:
            a_min, v_min = anom, x
    assert v_min < 100, f"could not parse anomaly anomaly type {type_name}"
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
