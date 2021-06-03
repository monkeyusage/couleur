from __future__ import annotations
from typing import Iterator
from PIL.Image import Image, open as im_open
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool
from sklearn.cluster import KMeans
from numba import njit

np.random.seed(0)


@njit
def luminance(red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> np.ndarray:
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def to_rgb(arr: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    red, green, blue = [arr[:, :, i].flatten() for i in range(3)]
    return red, green, blue


@njit
def hue(colors: np.ndarray) -> np.ndarray:
    arr = np.zeros(shape=5)
    colors /= 255
    for idx, rgb in enumerate(colors):
        delta = rgb.max() - rgb.min()
        if delta == 0:
            arr[idx] = 0
            continue
        max_color = rgb.argmax()
        if max_color == 0:  # red is max
            color_delta = 0 + (rgb[1] - rgb[2]) / delta
        elif max_color == 1:  # green is max
            color_delta = 2 + (rgb[2] - rgb[0]) / delta
        else:  # blue is max
            color_delta = 4 + (rgb[0] - rgb[1]) / delta
        value = color_delta * 60
        value = value if value >= 0 else value + 360
        arr[idx] = value
    return arr


@njit
def colorfulness(red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> float:
    # compute rg = R - G
    rg = np.absolute(red - green)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (red + green) - blue)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rb_mean, rb_std) = (np.mean(rg), np.std(rg))
    (yb_mean, yb_std) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    std_root = np.sqrt((rb_std ** 2) + (yb_std ** 2))
    mean_root = np.sqrt((rb_mean ** 2) + (yb_mean ** 2))
    # derive the "colorfulness" metric and return it
    return std_root + (0.3 * mean_root)


@njit
def complexity(arr: np.ndarray) -> float:
    ranges = np.arange(0, 390, 360 // 6)
    curr_max: int = 0
    counter: int = 0
    for idx, threshold in enumerate(ranges[1:]):
        prev_threshold = ranges[idx - 1]
        between: np.uint = ((arr > prev_threshold) & (arr < threshold)).sum()
        if between > 0:
            counter += 1
            if between > curr_max:
                curr_max = between
    if counter == 0:
        return 0
    out = curr_max / 5 / counter
    # out = np.log(1 + out)
    return out


def saturation(arr):
    maxs = np.max(arr, axis=1)
    mins = np.min(arr, axis=1)
    out = np.zeros_like(maxs, dtype=np.float32)
    np.divide(maxs - mins, maxs, out=out, where=(maxs != 0))
    return out


def batch_images(batch_size: int = 20) -> Iterator[list[tuple[str, np.ndarray]]]:
    counter = 0
    batch = []
    for root, _, files in os.walk(r"data\transforms"):
        for file in files:
            path: str = os.path.join(root, file)
            img: Image = im_open(path)
            arr: np.ndarray = np.asarray(img)
            if counter < batch_size:
                batch.append((file, arr))
                counter += 1
            else:
                yield batch
                counter = 0
                batch = []


def analyse(file: str, arr: np.ndarray) -> pd.DataFrame:
    print(f"Analysing {file}")
    kmeans = KMeans(n_clusters=5, max_iter=5, random_state=1)
    red, green, blue = to_rgb(arr)
    df: pd.DataFrame = pd.DataFrame({"r": red, "g": green, "b": blue})
    kmeans.fit(df)
    cred, cgreen, cblue = [kmeans.cluster_centers_[:, col] for col in range(3)]
    _, cluster_size = np.unique(kmeans.labels_, return_counts=True)
    summary = pd.DataFrame(
        {"red": cred, "green": cgreen, "blue": cblue, "size": cluster_size / 40_000}
    )
    summary["luminance"] = pd.Series(luminance(cred, cgreen, cblue))
    summary["hue"] = pd.Series(hue(summary[["red", "green", "blue"]].values))
    summary["colorfulness"] = colorfulness(cred, cgreen, cblue)
    summary["file"] = file
    summary["hue_complexity"] = complexity(summary["hue"].values)
    summary["saturation"] = saturation(summary[["red", "green", "blue"]].values)
    summary["contrast0"] = summary["luminance"].max() - summary["luminance"].min()
    summary["contrast1"] = summary["luminance"][3] - summary["luminance"][0]
    summary["contrast_groups"] = (
        summary["luminance"][-2:].mean() - summary["luminance"][:-2].mean()
    )
    weighted: np.ndarray = summary["luminance"].values * summary["size"].values
    summary["contrast_weighted"] = weighted[-1] - weighted[0]
    size_sum = summary["size"].sum()
    summary["contrast_weighted_groups"] = weighted[-2:].mean() - weighted[:-2].mean()
    summary["luminance_weighted"] = (
        summary["luminance"] * summary["size"]
    ).sum() / size_sum
    summary["saturation_weighted"] = (
        summary["saturation"] * summary["size"]
    ).sum() / size_sum
    summary["saturation_weighted_groups"] = (
        summary["saturation"][1:] * summary["size"][1:]
    ).sum() / summary["size"][1:].sum()
    return summary


def main() -> pd.DataFrame:
    dataframes = []
    with Pool(processes=(os.cpu_count() - 1)) as p:
        for batch in batch_images(batch_size=100):
            results = p.starmap(analyse, batch)
            dataframes.extend(results)
    dataframe : pd.DataFrame = pd.concat(dataframes)
    dataframe.to_csv("data/csv/analysis.tsv", sep="\t", index=False)
    return dataframe

if __name__ == "__main__":

