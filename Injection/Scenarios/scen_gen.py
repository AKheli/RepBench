import math
from pandas import DataFrame
import pandas as pd

from Injection.Scenarios.scenario import Scenario
from Injection.injected_data_part import InjectedDataContainer
import Injection.injection_config as ic
from Injection.injection_methods.injection import inject_data_df
from Injection.label_generator import generate_df_labels
from data_methods.data_class import DataContainer
import numpy as np


def create_injected_DataContainer(file_name, data_type, *, a_type, cols=None):
    """
    Parameters:
    file_name : str
    data_type: str "test" or "train"
    Returns InjectedDataContainer containing the injected dataframe every thing is normalized
    -------
    """
    data_container: DataContainer = DataContainer(file_name, data_type)
    data_df = data_container.norm_data.copy()
    injected_df, _ = inject_data_df(data_df, a_type=a_type, cols=cols)
    class_df = pd.DataFrame(np.invert(np.isclose(data_df.values, injected_df.values)),
                            columns=data_df.columns).reindex_like(injected_df)
    label_df: DataFrame = generate_df_labels(class_df)

    ##todo remove this once tested
    assert injected_df.index.equals(data_df.index), f"{injected_df.index},{data_df.index}"
    assert class_df.index.equals(data_df.index)
    assert label_df.index.equals(data_df.index)

    return InjectedDataContainer(injected_df, data_container.norm_data, class_df=class_df, name=data_container.title,
                                 labels=label_df)


from itertools import accumulate
def gen_a_rate_data(df, a_type, cols):
    a_percentages = ic.scenario_specifications["a_percentages"]
    max_perc = max(a_percentages)
    a_percentages = sorted(a_percentages)
    injected_df, col_range_mapper = inject_data_df(df, a_type=a_type, cols=cols, a_percent=max_perc)
    n, _ = df.shape

    ret_val = []  # (name,injected,truth)

    ### remove until anomaly ratio is lover than threshold
    col_range_mapper_rand = {col: np.random.permutation(index_list)
                             for col, index_list in col_range_mapper.items()}

    #assert False ,(cols, col_range_mapper)
    percentage_dict = {}
    for col in cols:
        column_ranges = col_range_mapper_rand[col]
        list_ratios =  list(accumulate(column_ranges, lambda b, a: b + len(a)/n*100, initial=0))
        list_ratios = np.array(list_ratios)
        last_index = 0.0
        for p in a_percentages:
            temp_df = percentage_dict.get(p,df.copy())
            percentage_dict[p] = temp_df
            idx = np.abs(list_ratios - p).argmin() #find closest ratio
            if last_index == idx:
                continue
            last_index = idx
            ranges_to_replace = column_ranges[:idx] #select all ranges under this ratio
            for range in ranges_to_replace:
                temp_df.iloc[range, col] = injected_df.iloc[range, col]

    ret_val = [(p,injected_df,df) for p,injected_df in percentage_dict.items()]
    return  ret_val


def gen_a_size_data(df, a_type, cols):
    assert a_type != "outlier"
    a_lengths = ic.scenario_specifications["a_lengths"]
    max_length = max(a_lengths)

    n_anomalies = math.ceil(df.shape[0] / 1000)

    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df, a_type=a_type,cols=cols,
                                                   n_anomalies=n_anomalies, a_len=max_length)

    ret_val = []
    for a_length in a_lengths[:-1]:
        temp_df = injected_df.copy()
        for col in cols:
            for index_range in col_range_mapper[col]:
                temp_df.iloc[index_range[a_length:]] = df.iloc[index_range[a_length:]]

        ret_val.append((a_length, temp_df, df))
        # plt.plot(temp_df.iloc[:, cols])
        # # plt.title(f"{counter},{n*ratio},{sum([len(arr) for arr in column_ranges[counter:]])}")
        # plt.show()
    ret_val.append((max_length, injected_df, df))
    return ret_val


def gen_ts_len_data(df, a_type, cols):
    ts_lengths_ratios = ic.scenario_specifications["length_ratios"]
    min_ratio = min(ts_lengths_ratios)
    n,m = df.shape
    offset = int((n-min_ratio*n)/2)
    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df, a_type=a_type,offset=offset)
    ret_val = []

    for ratio in ts_lengths_ratios[:-1]:
        off_set = int((n-n*ratio)/2)
        temp_df = injected_df.copy().iloc[off_set:-off_set,:]
        part_true_df = df.copy().iloc[off_set:-off_set,:]
        ret_val.append((ratio, temp_df, part_true_df))
    ret_val.append((1, injected_df, df))
    return ret_val


def gen_ts_nbr_data(df, a_type, cols):
    n_ts = ic.scenario_specifications["ts_nbrs"]
    injected_df = df.copy()
    injected_df, col_range_mapper = inject_data_df(injected_df,cols=[0], a_type=a_type)
    ret_val = []

    for n in n_ts:
        temp_df = injected_df.iloc[:,:n].copy()
        ret_val.append((n, temp_df, df.iloc[:,:n].copy()))
    return ret_val

def gen_a_factor_data(df, a_type, cols):
    a_factors = ic.scenario_specifications["a_factors"]
    a_factors = sorted(a_factors)
    ret_val = []
    minimal_factor = a_factors[0]

    seed = np.random.randint(1000)

    injected_df, col_range_mapper = inject_data_df(df.copy(), cols=cols, a_type=a_type, factor=minimal_factor,seed=seed)
    ret_val.append((minimal_factor, injected_df, df))
    for f in a_factors[1:]:
        temp_df , _  = inject_data_df(df.copy(), cols=cols, a_type=a_type , factor = f ,seed=seed)
        ret_val.append((f, temp_df ,df ))
    return ret_val

def gen_cts_nbr_data(df, a_type, cols):
    n_cts = ic.scenario_specifications["cts_nbrs"]
    n,m = df.shape
    full_injected_df = df.copy()
    full_injected_df, col_range_mapper = inject_data_df(full_injected_df,cols=list(range(m)), a_type=a_type)
    ret_val = []
    for m_c in sorted(n_cts):
        if m_c >= m:
            break
        temp_df = df.copy()
        temp_df.iloc[:,:m_c] = full_injected_df.iloc[:,:m_c]
        ret_val.append((m_c, temp_df, df))

    return ret_val


scen_generator_map = {
    ic.TS_NBR: gen_ts_nbr_data,
    ic.ANOMALY_SIZE : gen_a_size_data,
    ic.ANOMALY_RATE : gen_a_rate_data,
    ic.CTS_NBR :  gen_cts_nbr_data,
    ic.TS_LENGTH : gen_ts_len_data,
    ic.ANOMALY_FACTOR : gen_a_factor_data
}

def build_scenario(scen_name, file_name, data_type, a_type, max_n_rows=None, max_n_cols=None , cols = None):
    assert scen_name in ic.SCENARIO_TYPES, f"scenario {scen_name} must be one of {ic.SCENARIO_TYPES}"
    if max_n_rows is None:  max_n_rows = ic.MAX_N_ROWS
    if max_n_cols is None: max_n_cols = ic.MAX_N_COLS

    data_container: DataContainer = DataContainer(file_name, data_type , max_n_rows , max_n_cols)
    np.random.seed(10)
    n,m = data_container.norm_data.shape
    if cols == "all":
        cols = list(range(m))
    assert max(cols) < m , f"column numbers { [ i for i in cols if i >= m ]} to high for {m} columns"

    data_frame = data_container.norm_data

    cols_to_inject = cols if cols is not None else [0]
    scen_data = scen_generator_map[scen_name](data_frame,a_type,cols_to_inject)
    scenario = Scenario(scen_name,file_name,a_type , data_container= data_container )

    for (name,injected_df,data_df) in scen_data:
        #try:
            assert injected_df.index.equals(data_df.index), f"{injected_df.index},{data_df.index}"
            assert injected_df.shape == data_df.shape , f"{injected_df},{data_df}"

            class_df = pd.DataFrame(np.invert(np.isclose(data_df.values, injected_df.values))
                                    ,index=injected_df.index ,columns=injected_df.columns)

            assert class_df.isnull().sum().sum() == 0 , (data_df, )
            assert sum(class_df.sum(axis=0) != 0) == len(cols) , class_df.sum(axis=0)

            label_df: DataFrame = generate_df_labels(class_df)

            # plt.plot(injected_df.iloc[:,cols_to_inject])
            # plt.show()
            ##todo remove this once tested
            assert class_df.index.equals(data_df.index)
            assert label_df.index.equals(data_df.index)
            assert all(any(label_df.iloc[:,c]) for c in cols)
            assert injected_df.shape == data_df.shape
            injdected_container = InjectedDataContainer(injected_df,data_df, class_df=class_df,
                                         name=data_container.title,
                                         labels=label_df)
            scenario.add_part_scenario(injdected_container,name)
        #except Exception as e:
            #raise type(e)(str(e) + f'scen part: {name}')
    return  scenario
