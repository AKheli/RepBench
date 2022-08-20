
import numpy as np
from Scenarios.data_part import DataPart


def generate_data_part( injected,truth, * , train=None , label_rate = 0.2, name  = None, a_type =None  , data_check = True):
    assert injected.shape == truth.shape

    if data_check:
        assert injected.shape[0] > 100, injected.shape
        assert injected.shape[1] > 2, injected

    truth = truth.reset_index(drop=True)
    injected = injected.reset_index(drop=True)
    class_ =   truth.ne(injected)
    injected_bool =  class_.any()
    injected_columns = np.arange(len(injected_bool))[injected_bool]

    for col in injected_columns:
        x = np.array(injected)[:, col]
        y = np.array(truth)[:, col]
        assert not np.allclose(x, y)

    ## generate Labels
    if label_rate is not None:
        labels = class_.copy()
        for i, column_name in enumerate(labels):
            labels[column_name] = generate_column_labels(labels[column_name],label_rate)
    else:
        labels = class_.copy()

    return DataPart(injected=injected,truth=truth ,class_=class_, labels=labels ,  train=train , name=name, a_type=a_type)


def generate_column_labels(class_column, label_rate=0.2, label_anom_start=0.8):
    state = np.random.get_state()
    np.random.seed(100)
    labels = None
    for i in range(1000):
        starts = [min(r) for r in DataPart.get_anomaly_ranges(class_column) if len(r) > 1]
        m = len(class_column)
        r_number = np.random.uniform(size=m)
        r_number[starts] = r_number[starts] < label_anom_start
        r_number = r_number > 1 - label_rate
        labels = r_number.astype(bool)

        if np.any((class_column.astype(int) - labels) > 0) or not np.any(
                class_column.astype(int)):  # make there are non labeled data points
            break

    np.random.set_state(state)
    return labels


def get_cutted_part(data_part : DataPart, columns):
    if isinstance(columns, int):
        columns = np.arange(columns)

    cutted_injected = data_part.injected.iloc[:,columns]
    cutted_truth = data_part.truth.iloc[:,columns]
    cutted_class = data_part.class_.iloc[:,columns]
    cutted_labels = data_part.labels_.iloc[:,columns]
    name = data_part.name
    a_type = data_part.a_type
    train =  data_part.train

    cutted_train = None
    if train is not None:
        cutted_train = get_cutted_part(train,columns)

    return DataPart(injected=cutted_injected, truth=cutted_truth, class_=cutted_class, labels=cutted_labels, train=cutted_train, name=name, a_type=a_type)
