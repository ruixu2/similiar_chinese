import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import *
import skimage as ski


def get_similiar(path1, path2):
    image1 = ski.io.imread(path1, as_gray=True)
    image2 = ski.io.imread(path2, as_gray=True)
    # 计算结构相似性指数
    similarity_index = ssim(image1, image2, data_range=1.0)
    # similarity_index=normalized_root_mse(image1,image2)
    return similarity_index


if __name__ == '__main__':
    chinese_list = []
    for i in range(0x4E00, 0x9FA5 + 1):
        temp = chr(i)
        chinese_list.append((i, temp))
    for idx, item in enumerate(chinese_list):
        idx1 = item[0]
        i1 = item[1]
        img_path1 = f"../img/{idx1}" + "_" + i1 + ".jpg"
        for item2 in chinese_list[idx + 1:]:
            idx2 = item2[0]
            i2 = item2[1]
            img_path2 = f"../img/{idx2}" + "_" + i2 + ".jpg"
            similarity = get_similiar(img_path1, img_path2)
            if similarity > 0.85:
                print(img_path1, img_path2)
                print(similarity)
