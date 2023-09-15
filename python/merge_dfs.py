import pandas as pd


def read_txt(category: str) -> pd.DataFrame:
    with open(f"data/csv/{category}_class.txt", "r") as f:
        lines = f.read().split("\n")
        df = pd.DataFrame(
            [line.split(" ") for line in lines], columns=["class", category]
        ).dropna()
        df["class"] = df["class"].astype(int)
    return df


def read_csv(category: str) -> pd.DataFrame:
    load = lambda dataset: pd.read_csv(
        f"data/csv/{category}_{dataset}.csv", header=None, names=["img", "class"]
    )
    dfs = map(load, ("train", "val"))
    return pd.concat(dfs, axis=0)


def read(category: str) -> pd.DataFrame:
    txt = read_txt(category)
    df = read_csv(category)
    return pd.merge(df, txt, on="class", how="left").drop("class", axis=1)


CATEGORIES = ("artist", "genre", "style")

artist, genre, style = [read(category) for category in CATEGORIES]
main_df = style.merge(genre, on="img", how="left")
main_df = main_df.merge(artist, on="img", how="left")

main_df.to_csv("data/csv/data.tsv", sep="\t", index=False)
