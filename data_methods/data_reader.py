import os
import pandas as pd

default_data_folder = "data"

def read_data(data_name, folder=default_data_folder):
    files_in_folder = [f for f in os.listdir(folder) if os.path.isfile(f"{folder}/{f}")]
    assert len(files_in_folder) > 0, os.listdir(folder)
    possible_files = [f for f in files_in_folder if f.startswith(data_name)]
    assert len(possible_files) == 1, f"{data_name} could not be from possible files {files_in_folder} in {folder} , got {possible_files}"

    file_path = f"{folder}/{possible_files[0]}"

    ## check if first row are headrs or numerical values belongin to the dataset
    first_row = pd.read_csv(file_path, nrows=1, header=None, sep=",")
    float_in_first_row = any([isinstance(x, float) for x in first_row.values])
    header = None if float_in_first_row else 0

    data_df = pd.read_csv(file_path, header=header, sep=",")

    return data_df


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


def train_test_read(data_name, max_n_rows=None, max_n_cols=None, folder=default_data_folder, normalize=True, split=0.5):
    data = read_data(data_name, folder=folder)
    n, m = data.shape
    if max_n_rows is None: max_n_rows = n
    if max_n_cols is None: max_n_cols = m

    if split is not None:
        split = int(n * split)
        train = data.iloc[max(0, split - 2000):split, : min(max_n_cols, m)]
        test = data.iloc[split:min(n, split + max_n_rows), : min(max_n_cols, m)]

        if normalize:
            train = (train - train.mean()) / train.std()
            test = (test - test.mean()) / test.std()

    return train.reset_index(drop=True), test.reset_index(drop=True)


def data_sets(folder="data"):
    data_dir = os.listdir("data")
    data_files = [f for f in data_dir if os.path.isfile(f"{folder}/{f}") and not f.endswith(".md")]
    return data_files

