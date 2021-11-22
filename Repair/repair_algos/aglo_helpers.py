import numpy as np

def generate_labels(series, proportion ,anomaly_info = None , first_labels = 5 , start_of_anomaly = 3):
    assert proportion < 1 and proportion >= 0 , "invalid label proportion must be between 0 and 1"

    length = series
    try:
        length = len(series)
    except:
        assert length.isdigit() , " could not infer series length"

    labels = list(range(first_labels))
    if anomaly_info is not None:
        for k , v in anomaly_info.items:
            labels.append(anomaly_info[k]['index_range'][:start_of_anomaly])
    label_amount = int(length*proportion)

    labels += list(np.random.randint(first_labels, length-2 , label_amount - len(labels)))
    return np.array(labels)