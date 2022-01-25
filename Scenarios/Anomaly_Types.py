AMPLITUDE_SHIFT = "amplitude_shift"
DISTORTION = "distortion"
GROWTH_CHANGE = "growth_change"
POINT_OUTLIER = "point_outlier"

ANOMALY_TYPES = (AMPLITUDE_SHIFT,
                 DISTORTION,
                 GROWTH_CHANGE,
                 POINT_OUTLIER)


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
