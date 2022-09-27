from Injection.injection_config import ANOMALY_TYPES, BASE_FACTORS, BASE_ANOMALY_SETTINGS
from Injection.injection_methods.basic_injections import add_anomalies



def inject_data_df(data_df, *, a_type, cols=None, offset=10, factor = None
                   , n_anomalies_or_percentage = BASE_ANOMALY_SETTINGS["a_percentage"],
                   a_len = BASE_ANOMALY_SETTINGS["a_length"],
                   ignore_warnings = False):
    assert a_type in ANOMALY_TYPES
    assert n_anomalies_or_percentage > 0
    if factor is None :
        factor = BASE_FACTORS[a_type]

    if  1 > n_anomalies_or_percentage:
        n_anomalies = int(n_anomalies_or_percentage*data_df.shape[0]/a_len)+1
    else:
        n_anomalies = n_anomalies_or_percentage

    assert n_anomalies - int(n_anomalies) == 0

    columns_to_inject = [0] if cols is None else cols

    injected_df = data_df.copy()
    col_ranges_mapper = {}
    for col in columns_to_inject:
        injected_df.iloc[:, col] , index_ranges = add_anomalies(injected_df.iloc[:, col], a_type, offset=offset, a_factor=factor,
                                                 n_anomalies=n_anomalies , a_len=a_len)
        col_ranges_mapper[col] = index_ranges

    assert injected_df.shape == data_df.shape
    assert injected_df.index.equals(data_df.index)
    return injected_df , col_ranges_mapper



