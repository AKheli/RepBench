import math
import numpy as np
import pandas as pd
import Scenarios.ScenarioConfig as sc
import Scenarios.AnomalyConfig as ac

from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_random_indices
import Scenarios.data_part_generator as pg
from data_methods.Helper_methods import get_df_from_file

def normalize_f(X):
    """
    Parameters: matrix X
    Returns: normalized X , normalization_inverse function
    """
    mean_X, std_X = X.mean(), X.std()
    assert (len(mean_X), len(std_X)) == (X.shape[1], X.shape[1])

    def inv_func(X_norm):
        X_norm.columns = X.columns
        result = X_norm * std_X + mean_X
        return result

    return (X - mean_X) / std_X, inv_func

def generate_scenario_data(scen_name, data, a_type,cols_to_inject=None, train_test_split=0.5,  normalize=True):
    print("anomlaly_type" , a_type)
    assert scen_name in sc.SCENARIO_TYPES, f"scenario {scen_name} must be one of {sc.SCENARIO_TYPES}"

    data = data if isinstance(data, pd.DataFrame) else get_df_from_file(data)[0]
    cols_to_inject = cols_to_inject if cols_to_inject is not None else [0]

    n, m = data.shape
    split = int(n * train_test_split)

    max_n_rows = sc.MAX_N_ROWS if sc.MAX_N_ROWS is not None else split + 1

    train = data.iloc[max(0, split - 2000):split, : min(sc.MAX_N_COLS, m)]
    test = data.iloc[split:min(n, split + max_n_rows), : min(sc.MAX_N_COLS, m)]

    if normalize:
        train = (train - train.mean()) / train.std()
        test = (test - test.mean()) / test.std()


    result = {}
    np.random.seed(10)

    scen_spec = sc.scenario_specifications[scen_name]
    base_spec = sc.scenario_specifications[sc.BASE_SCENARIO]

    ## create trainings scenario
    a_length = base_spec["a_length"]
    a_perc = base_spec["a_percentage"]

    train_injected = train.copy()
    for col in cols_to_inject:
        train_injected.iloc[:, col], indices = inject_single(train_injected.iloc[:, col], a_type, a_length,
                                                             percentage=a_perc*2)
    train_part = pg.generate_data_part(train_injected,train,train=None,name = scen_name , a_type=a_type)

    ## create specified scenarios


    if scen_name == sc.BASE_SCENARIO:
        a_length = scen_spec["a_length"]
        a_perc =  scen_spec["a_percentage"]
        test_injected = test.copy()
        for col in cols_to_inject:
            test_injected.iloc[:, col], indices = inject_single(test_injected.iloc[:, col], a_type, a_length,percentage=a_perc)
        result[len(indices)] = pg.generate_data_part(test_injected, test, train=train_part, name=scen_name, a_type=a_type)


    if scen_name == sc.ANOMALY_RATE:
        a_length = scen_spec["a_length"]
        for a_perc in scen_spec["a_percentages"]:
            test_injected = test.copy()
            for col in cols_to_inject:
                test_injected.iloc[:, col], indices = inject_single(test_injected.iloc[:, col], a_type, a_length,
                                                                    percentage=a_perc)
            assert len(indices) != 0
            result[len(indices)] = pg.generate_data_part(test_injected, test, train= train_part,name = scen_name , a_type=a_type)

    if scen_name == sc.ANOMALY_SIZE:
        a_lengths = scen_spec["a_lengths"]
        n_anomalies = math.ceil(n/1000)
        for a_length in a_lengths:
            test_injected = test.copy()
            a_indices = {}
            for col in cols_to_inject:
                test_injected.iloc[:, col], indices = inject_single(test_injected.iloc[:, col],a_type=  a_type,
                                                                    anomaly_amount=n_anomalies, anomaly_length=a_length)
                a_indices[col] = indices
            result[a_length] = pg.generate_data_part(test_injected, test,train=train_part,name = scen_name , a_type=a_type)

    if scen_name == sc.TS_LENGTH:
        ts_length_percentages = scen_spec["length_percentages"]
        a_perc = scen_spec["a_percentage"]
        a_length = scen_spec["a_length"]
        test_injected = test.copy()
        n, m = test.shape
        half_start = int(ts_length_percentages[0] / 100 / 2 * n)
        center = math.floor(n / 2)

        #inject center
        for col in cols_to_inject:
            start, stop = center - half_start, center + half_start
            test_injected.iloc[start:stop, col], indices = inject_single(
                test_injected.iloc[start:stop, col], a_type = a_type,anomaly_length=a_length, percentage=a_perc)

        #add values to the right and the left of the series
        for perc in ts_length_percentages:
            test_injected = test_injected.copy()
            n_half = math.ceil(perc/100 / 2 * n,)
            start, stop = center - n_half+1, center + n_half
            result[stop-start] = pg.generate_data_part(test_injected.iloc[start:stop], test.iloc[start:stop],train=train_part
                                    ,name = scen_name , a_type=a_type)

    if scen_name == sc.TS_NBR:
        a_perc = scen_spec["a_percentage"]
        a_length = scen_spec["a_length"]
        n_ts = scen_spec["ts_nbrs"]

        test_injected = test.copy()
        for col in cols_to_inject:
            test_injected.iloc[:, col], anomaly_infos = inject_single(
                np.array(test_injected.iloc[:, col]),a_type = a_type, anomaly_length=a_length, percentage=a_perc)

        full_data_part = pg.generate_data_part(test_injected, test.copy(), train=train_part,name = scen_name , a_type=a_type)

        for ts_nbr in [n for n in n_ts if n <= test.shape[1]]:
            result[ts_nbr] = pg.get_cutted_part(full_data_part,ts_nbr)

    if scen_name == sc.CTS_NBR:
        a_perc = scen_spec["a_percentage"]
        a_length = scen_spec["a_length"]
        n_contaminated_series = scen_spec["cts_nbrs"]
        assert len(set(n_contaminated_series)) == len(n_contaminated_series)

        # inject all series
        injected = test.copy()
        for col in [n for n in n_contaminated_series if n <= test.shape[1]]:
            injected.iloc[:, col-1], anomaly_infos = inject_single(
                np.array(test.iloc[:, col-1]),a_type = a_type, anomaly_length=a_length, percentage=a_perc)

        for cts_nbr in [n for n in n_contaminated_series if n <= injected.shape[1]]:
            injected_part = test.copy()
            injected_part.iloc[:,:cts_nbr] = injected.iloc[:,:cts_nbr]
            data_part = pg.generate_data_part(injected_part, test.copy(), train=train_part,name = scen_name , a_type=a_type)
            result[cts_nbr] = data_part
            assert len(data_part.injected_columns) == cts_nbr
    return result


def inject_single(data, a_type, anomaly_length, anomaly_amount=None, percentage=None):
    assert percentage is not None or anomaly_amount is not None, "number of anomalies or anomalypercentage must be specified"

    if percentage is not None:
        if a_type == ac.POINT_OUTLIER:
            anomaly_length = 1
        index_ranges = get_random_indices(data, anomaly_length, percentage=percentage)
    else:
        if a_type == ac.POINT_OUTLIER:
            anomaly_amount = anomaly_amount * anomaly_length
            anomaly_length = 1
        index_ranges = get_random_indices(data, anomaly_length, number_of_ranges=anomaly_amount)

    assert len(index_ranges) != 0
    for range_ in index_ranges:
        assert len(range_) != 0
        assert max(range_) < len(data), (len(data), index_ranges)
        assert a_type == ac.POINT_OUTLIER or len(range_) > 1

        data, _ = add_anomaly(anomaly_type=a_type, data=data, index_range=range_)
    return data, index_ranges


