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


def get_cur_date() -> str:
    return time.strftime("%Y%m%d", time.localtime())


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


@app.route('/saveconsinfo', methods=['POST'])
def print_dcit():
    print("收到信息！")
    try:
        info_table = request.form
        json_tosave = {}
        for key in info_table:
            print(key, '\t', info_table[key])
            json_tosave[key] = info_table[key]
        new_json_string = json.dumps(json_tosave, ensure_ascii=False)  # 正常显示中文
        with open(save_dir + f"test_{info_table['filename']}.json", 'w', encoding='utf_8') as nf:
            nf.write(new_json_string)
        response = {'code': 0, 'message': "table form received successfully!"}

        return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)


@app.route('/saveaudio', methods=['POST'])
def save_audio():
    print("get request...")
    # print(request.files)
    # print(request.form)
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空部分，没有文件名
    if file.filename == '':
        return 'No selected file', 400
    ext = file.filename.split('.')[-1]
    if file:
        # file.save("./uploads/temp.m4a")
        # audio_file_path = "./uploads/temp.m4a"
        audio_file_path = "./recorded_audio/" + request.form['filename'] + "."+ext
        print("savepath:", audio_file_path)
        file.save(audio_file_path)
        result = {
            'code': 200
        }
        return jsonify(result)

    else:
        return 'Only M4A files are allowed', 400


@app.route('/savectmcinfo', methods=['POST'])
def save_info():
    print("收到信息！")
    try:
        info_table = request.get_json()
        print(info_table)
        json_tosave = {}
        for key in info_table:
            print(key, '\t', info_table[key])
            json_tosave[key] = info_table[key]
        new_json_string = json.dumps(json_tosave, ensure_ascii=False)  # 正常显示中文
        with open(save_dir + f"ctm_data_{info_table['filename']}.json", 'w', encoding='utf_8') as nf:
            nf.write(new_json_string)
        response = {'code': 0, 'message': "table form received successfully!"}

        return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)


# if __name__ == '__main__':
#     print(get_cur_date())


if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
