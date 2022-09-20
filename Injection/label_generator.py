import Injection.injection_config as ic
import numpy as np


def get_anomaly_ranges(ts_class):
    in_anomaly = False
    ranges = []
    current_range = []
    for i, v in enumerate(ts_class):
        if v:
            in_anomaly = True
            current_range.append(i)
        if not v:
            if in_anomaly:
                in_anomaly = False
                ranges.append(current_range)
                current_range = []
    return [np.array(range_) for range_ in ranges]



def generate_df_labels(class_df, seed= None):
    label_df = class_df.copy()

    for (i,column) in enumerate(label_df):
        label_df[column] = generate_column_labels(class_df[column], seed=i+(0 if seed is None else seed))

    return label_df

def generate_column_labels(class_column , seed=None):
    label_rate =  ic.label_rate
    label_anom_start = ic.anomstartlabelrate
    state = np.random.get_state()
    np.random.seed(ic.label_seed + (seed if seed is not None else 0))
    labels = None
    for i in range(1000):
        starts = [min(r) for r in get_anomaly_ranges(class_column) if len(r) > 1]
        m = len(class_column)
        r_number = np.random.uniform(size=m)
        r_number[starts] = r_number[starts] < label_anom_start
        r_number = r_number < label_rate
        labels = r_number.astype(bool)
        if np.any((class_column.astype(int) - labels) > 0) or not np.any(
                class_column.astype(int)):  # make there are non labeled data points
            break

    np.random.set_state(state)
    return labels



