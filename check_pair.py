#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/10/9 20:20
# @Author: ZhaoKe
# @File : check_pair.py
# @Software: PyCharm
import os

DATA_DIR = "F:/NEUCTMDATASET/20240929-1008/"


def check_pairs():
    ctmc_list = []
    cond_list = []
    kv_pair = dict()
    for item in os.listdir(DATA_DIR):
        if item[:3] == "ctm":
            ctmc_list.append(item[9:23])
        elif item[:4] == "test":
            cond_list.append(item[5:19])
        else:
            continue
    print(len(ctmc_list), len(cond_list))
    marked1 = [True for _ in ctmc_list]  # *
    marked2 = [True for _ in cond_list]  # *
    sorted(ctmc_list)
    sorted(cond_list)
    for i, item in enumerate(cond_list):
        for j, jtem in enumerate(ctmc_list):
            if item == jtem:
                kv_pair[item] = jtem
                marked1[j] = False
                marked2[i] = False
                break
    print(marked1)
    print(marked2)
    print("=================ctm===============")
    for j in range(len(marked1)):
        if marked1[j]:
            print(ctmc_list[j])
    print("==================condi===========")
    for i in range(len(marked2)):
        if marked2[i]:
            print(cond_list[i])
    for k, v in kv_pair.items():
        print(k, v)
    print(len(kv_pair))


if __name__ == '__main__':
    check_pairs()
