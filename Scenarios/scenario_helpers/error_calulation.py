import pandas as pd


def calculate_errors( truth, injected, repairs, columns , error_func):
    errors = {"original_error": error_func(truth, injected, columns)}
    for algo_name, algo_output in repairs.items():
        errors[algo_name] = error_func(truth, algo_output["repair"],columns, algo_output.get("labels", None))
    return errors

def generate_error_df(values,  error_func):
    df = pd.DataFrame()
    for k, v in values.items():
        truth = v.get("truth",None) if v.get("truth",None) is not None else v.get("original",None)
        assert truth is not None
        injected = v["injected"]
        df = df.append(pd.Series(calculate_errors(truth, injected, v["repairs"],v["columns"], error_func), name=k))
    return df

