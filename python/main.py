from __future__ import annotations
from typing import Iterator
from pandas import read_csv, DataFrame
import numpy as np
from numba import njit
import cv2

@njit
def pad_rgb_img(img:np.ndarray, max_size:np.uint8) -> np.ndarray:
	height, width, _ = img.shape
	# create new image of desired size and color (white) for padding
	background = np.multiply(np.ones(shape=(max_size, max_size, 3), dtype=np.uint8), 255)
	# compute center offset
	x_center = np.uint8((max_size - width) // 2)
	y_center = np.uint8((max_size - height) // 2)
	# copy img image into center of result image
	background[y_center:y_center+height, x_center:x_center+width] = img
	return background

def iter_batch(df:DataFrame, batch_size:int) -> Iterator[np.ndarray[np.ndarray]]:
	idx = 0
	batch = []
	for img in df['img']:
		if idx >= batch_size:
			max_size = np.max([img.shape for img in batch])
			imgs = np.array([pad_rgb_img(img, max_size) for img in batch], dtype=np.uint8)
			yield imgs
			# reset current batch & idx
			batch = []
			idx = 0
		idx += 1
		raw_img = cv2.imread(f"data/img/{img}")
		batch.append(raw_img)

if __name__ == "__main__":
	df : DataFrame = read_csv("data/csv/data.tsv", sep="\t")
	for batch in iter_batch(df=df, batch_size=10):
		for img in batch:
			cv2.imshow("img", img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		break