import numpy as np

def generate_labels(injected, truth = None ,  label_ratio = 0.2  , first_labels = 5 , start_of_anomaly = 3):
    assert label_ratio < 1 and label_ratio >= 0 , "invalid label proportion must be between 0 and 1"

    length = len(injected)
    labels = np.zero_like(injected)
    labels[:first_labels] = 1

    if truth is not None:
        anomalies = np.invert(np.isclose(injected,truth))
        anomalies[0] = False
        anomalies[-1] = False
        diffs = np.diff(anomalies)
        args = np.argwhere(diffs)
        anomaly_starts = args[::2] + 1
        for i in range(start_of_anomaly):
            labels[anomaly_starts+i] = 1

    still_to_inject = labels == 0
    amount_to_add = len(labels)*label_ratio - (labels == 1)
    possible_indices = np.arange(len(labels))[still_to_inject]
    choosen_indices =  np.random.choice(possible_indices,replace=False,size=amount_to_add)
    labels[choosen_indices]=1

    return np.arange(len(labels))[labels]