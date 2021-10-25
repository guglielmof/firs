import pandas as pd


def pandas_csv_reader(path):
    return pd.read_csv(path, sep=";", names=["qid", "query"])
