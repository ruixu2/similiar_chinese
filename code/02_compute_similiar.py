import numpy as np
import os

import pandas as pd
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import *
import skimage as ski
import multiprocessing as mp
import json


def get_similiar(path1, path2):
    image1 = ski.io.imread(path1, as_gray=True)
    image2 = ski.io.imread(path2, as_gray=True)
    # 计算结构相似性指数
    similarity_index = ssim(image1, image2, data_range=1.0)
    # similarity_index=normalized_root_mse(image1,image2)
    return similarity_index


def save_similair(idx1, i1, chinese_list, ):
    img_path1 = f"../img/{idx1}" + "_" + i1 + ".jpg"
    for item2 in chinese_list:
        idx2 = item2[0]
        i2 = item2[1]
        img_path2 = f"../img/{idx2}" + "_" + i2 + ".jpg"
        similarity = get_similiar(img_path1, img_path2)
    print(f"../similiar/{idx1}_{i1}.csv")


def read_all_res():
    df_list = []
    item_list = os.listdir("../result/")
    if len(item_list) == 0:
        df = pd.DataFrame(columns=['char1', 'code1', "char2", "code2", "similarity"])
        return df
    for item in item_list:
        if item.endswith("csv"):
            df_list.append(pd.read_csv(f"../result/{item}"))
    return pd.concat(df_list)


def split_and_save_df(df):
    pass


def get_finished():
    if not os.path.exists("../finished.txt"):
        finished_f = open("../finished.txt", mode='w', encoding="utf-8")
        finished_list = []
    elif os.path.exists("../finished.txt"):
        finished_f = open("../finished.txt", mode='r', encoding="utf-8")
        finished_list = finished_f.readlines()
        finished_set = set(finished_list)
        finished_f = open("../finished.txt", mode='w', encoding="utf-8")
    return finished_f, finished_set


def get_chinese_list():
    chinese_list = []
    for i in range(0x4E00, 0x9FA5 + 1):
        temp = chr(i)
        chinese_list.append((i, temp))
    return chinese_list


if __name__ == '__main__':
    # all_res_df = read_all_res()
    finished_f, finished_set = get_finished()
    print(f"finished: {len(finished_set)}")
    chinese_list = get_chinese_list()
    print(f"len of chinese char: {len(chinese_list)}")
    p = mp.Pool(8)
    for idx, item in enumerate(chinese_list[:20000]):
        if idx % 1000 == 0:
            print(idx)
        idx1 = item[0]
        i1 = item[1]
        if os.path.exists(f"../similiar/{idx1}_{i1}.csv") or (f"{idx1}_{i1}" in finished_set):
            if (f"{idx1}_{i1}" not in finished_set):
                finished_set.add(f"{idx1}_{i1}")
        else:
            p.apply_async(save_similair, args=(idx1, i1, chinese_list,))
            finished_set.add(f"{idx1}_{i1}")
    for item in finished_set:
        finished_f.write(f"{item}\n")
    finished_f.close()
    # all_res_df.to_csv(f"../result/similiar.csv", index=False)
    p.close()
    p.join()
