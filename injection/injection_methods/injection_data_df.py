import math
from injection.injection_config import BASE_FACTORS, POINT_OUTLIER, BASE_PERCENTAGES, DEFAULT_LENGTH
from injection.injection_methods.basic_injections import add_anomalies


def inject_data_df(data_df, *, a_type, cols=None, offset=10,
                   factor=None, a_percent=None, n_anomalies=None,
                   a_len=None, index_range_col_mapper=None, seed=None):

    if factor is None:
        factor = BASE_FACTORS[a_type]
    if a_percent is None:
        a_percent = BASE_PERCENTAGES[a_type]
    if a_len is None:
        a_len = 1 if a_type == POINT_OUTLIER else DEFAULT_LENGTH
    if n_anomalies is None:
        assert a_percent > 0
        n_anomalies = math.floor(a_percent / 100 * data_df.shape[0] / a_len) + 1

    assert n_anomalies - int(n_anomalies) == 0
    print("select columns")

    columns_to_inject = [0] if cols is None else cols
    injected_df = data_df.copy()
    col_ranges_mapper = {}
    for col in columns_to_inject:
        print(f"inject col: {col}")
        injected_df.iloc[:, col], index_ranges = add_anomalies(injected_df.iloc[:, col], a_type, offset=offset,
                                                               a_factor=factor,
                                                               n_anomalies=n_anomalies, a_len=a_len,
                                                               index_ranges=None if
                                                               index_range_col_mapper is None else
                                                               index_range_col_mapper[col], seed=seed)
        print("injected_df.shape", injected_df.shape)
        col_ranges_mapper[col] = index_ranges
    print("injected_df.shape", injected_df.shape)
    assert injected_df.shape == data_df.shape
    assert injected_df.index.equals(data_df.index)
    return injected_df, col_ranges_mapper
