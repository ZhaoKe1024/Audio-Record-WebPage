#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 15:23
# @Author: ZhaoKe
# @File : install_packages.py
# @Software: PyCharm
import os
pack_list = [
    # "PyQT5",
    # "click~=7.0",
    # "pyinstaller==6.6.0",
    # "pyqt-tools",

    # "pyaudio"
    # "playsound",
    # "FFmpeg"

    # "openpyxl",

    "pymysql"
]
# set DS_BUILD_AIO=0
# set DS_BUILD_SPARSE_ATTN=0
for packa in pack_list:
    # os.system("pip install " + packa + " -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system("pip install " + packa + " -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com")
