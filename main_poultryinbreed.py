#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 14:30
# @Author: ZhaoKe
# @File : main_poultryinbreed.py
# @Software: PyCharm
import os
import json
import time
from flask import Flask, request, jsonify, render_template
from databasekits.table_packets import insert_use_dict
from gevent import pywsgi

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'

CHUNK_SIZE = 1024 * 1024
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M
form_save_mode = 0  # mysql 0, local json file 1,

save_dir = "./temp_files/"


def get_cur_timestr() -> str:
    return time.strftime("%Y%m%d%H%M", time.localtime())


@app.route('/')
def index():
    return render_template("./main_poultryinbreed.html")



if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
