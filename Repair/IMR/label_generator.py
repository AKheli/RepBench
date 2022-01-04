import numpy as np

def generate_anomaly_start_labels(injected, truth, start_of_anomaly = 3):
    injected = np.array(injected)
    labels = np.zeros_like(injected)

    truth = np.array(truth)
    anomalies = np.invert(np.isclose(injected, truth))
    anomalies[0] = False
    anomalies[-1] = False
    diffs = np.diff(anomalies)
    args = np.argwhere(diffs)
    anomaly_starts = args[::2]
    for i in range(start_of_anomaly):
        labels[anomaly_starts + i] = 1

    return labels

def generate_random_labels(injected , label_ratio = 0.2  , first_labels = 5 , already_labeled = None):
    assert label_ratio < 1 and label_ratio >= 0 , "invalid label proportion must be between 0 and 1"
    injected = np.array(injected)
    if already_labeled is None:
        labels = np.zeros_like(injected)
    else:
        labels = already_labeled

    labels[:first_labels] = 1

    still_to_inject = labels == 0
    amount_to_add = int(len(labels)*label_ratio - sum((labels == 1)))
    if amount_to_add >0:
        possible_indices = np.arange(len(labels))[still_to_inject]
        choosen_indices =  np.random.choice(possible_indices,replace=False,size=amount_to_add)
        labels[choosen_indices]=1

    return np.arange(len(labels))[labels.astype(bool)]