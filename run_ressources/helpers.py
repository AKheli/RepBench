def split_data_set(df, split=0.5):
    split = int(len(df[df.columns[0]]) * split)
    train, test = df.iloc[:split, :], df.iloc[split:, :]
    return train, test
