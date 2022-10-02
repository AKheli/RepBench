import pandas as pd
import os

default_data_folder = "data"

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


def infer_data_file(file_name,folder):
    files_in_folder = [f for f in os.listdir(folder) if os.path.isfile(f"{folder}/{f}")]
    assert len(files_in_folder) > 0, os.listdir(folder)
    possible_files = [f for f in files_in_folder if f.startswith(file_name)]
    assert len(possible_files) == 1, f"{file_name} could not be from possible files {files_in_folder} in {folder} , got {possible_files}"
    file_path = f"{folder}/{possible_files[0]}"
    return file_path


def read_data(data_name, folder):
    curr_wd = os.getcwd()
    root_dir = "RepairBenchmark"
    os.chdir("".join(curr_wd.split(root_dir)[:-1])+root_dir)
    file_path = infer_data_file(data_name,folder)
    ## check if first row are headrs or numerical values belongin to the dataset
    first_row = pd.read_csv(file_path, nrows=1, header=None, sep=",")
    float_in_first_row = any([isinstance(x, float) for x in first_row.values])
    header = None if float_in_first_row else 0

    data_df = pd.read_csv(file_path, header=header, sep=",")
    os.chdir(curr_wd)

    return data_df


class DataContainer():
    def __init__(self, file_name, type="train" , max_n_rows = None , max_n_cols = None):
        assert type in ["train", "test"]
        data_df = read_data(file_name,folder="data/"+type)

        n,m = data_df.shape
        if max_n_rows is None : max_n_rows = n
        if max_n_cols is None : max_n_cols = m

        data_df = data_df.iloc[:max_n_rows, :max_n_cols]

        self.original_data = data_df
        self.type = type
        self.title = file_name
        self.norm_data, self.inf_norm_f = normalize_f(self.original_data)
        self.injected = None

