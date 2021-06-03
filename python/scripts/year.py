import pandas as pd

dataframe = pd.read_csv("data/csv/data.tsv")

if not "year" in dataframe.columns:
    dataframe["year"] = dataframe["img"].str.extract(r"(\d{4})")[0]
    dataframe["year"] = dataframe["year"].fillna(pd.NA)

dataframe.to_csv("data/csv/data.tsv", sep="\t", index=False)
