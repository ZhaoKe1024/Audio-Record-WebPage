#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/8/15 15:33
# @Author: ZhaoKe
# @File : ctmc_collect.py
# @Software: PyCharm
import os
import json
import time
from flask import Flask, request, jsonify, render_template
from gevent import pywsgi

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'

CHUNK_SIZE = 1024 * 1024
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M
form_save_mode = 0  # mysql 0, local json file 1,

save_dir = "./ctmc_files/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)


def get_cur_timestr() -> str:
    return time.strftime("%Y%m%d%H%M", time.localtime())


@app.route('/')
def index():
    return render_template("./tizhidiaocha.html")


file_cnt = len(os.listdir(save_dir)) - 1


def get_name():
    global file_cnt
    print("current count of files:", file_cnt)
    file_cnt += 1
    return file_cnt


@app.route('/get_info', methods=['POST'])
def print_dcit():
    print("收到信息！")
    try:
        info_table = request.get_json()
        print(info_table)
        json_tosave = {}
        for key in info_table:
            print(key, '\t', info_table[key])
            json_tosave[key] = info_table[key]
        new_json_string = json.dumps(json_tosave, ensure_ascii=False)  # 正常显示中文
        with open(save_dir + f"ctm_data_{get_name()}.json", 'w', encoding='utf_8') as nf:
            nf.write(new_json_string)
        response = {'code': 0, 'message': "table form received successfully!"}

        return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)


if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
