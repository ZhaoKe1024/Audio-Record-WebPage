#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:51
# @Author: ZhaoKe
# @File : main.py
# @Software: PyCharm
import base64

import numpy as np
import soundfile
from flask import Flask, request, jsonify, render_template
from flask_uploads import UploadSet, configure_uploads, patch_request_class
from databasekits.table_packets import insert_use_dict

app = Flask(__name__)
from app import routes

# # 配置文件上传
# app.config['UPLOADS_DEFAULT_DEST'] = 'static/uploads'
# app.config['UPLOADS_DEFAULT_URL'] = '/static/uploads'
# app.config['UPLOADSet'] = ('my_uploads', 'uploads', 'all')

# 初始化上传套件
# my_uploads = UploadSet(app)
# configure_uploads(app, my_uploads)
# patch_request_class(app)  # 据说默认16MB
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M
patch_request_class(app, MAX_CONTENT_LENGTH)


@app.route('/')
def index():
    return render_template("./index.html")
    # return "<p>hello world</p><br><p>ok!</p>"


# 定义上传音频文件的路由
@app.route('/getdata', methods=['POST'])
def upload():
    info_table = request.form
    print(info_table['jsondata'])
    samples = np.frombuffer(info_table['audio'], dtype=np.int16)
    fname = "test_audio_000.wav"
    soundfile.write(
        f"./audio/{fname}",
        samples,
        16000,
        format='WAV',
        subtype="FLOAT")
    # audio_file = request.files['audio']
    # 将音频文件保存到服务器上的指定路径
    # audio_file.save('./audio/test_audio_000.wav')
    resp_message = "Data received successfully!\n"
    info_table['filename'] = fname
    insert_use_dict(info_table)
    resp_message += "Data insert into database successfully!"
    response = {'message': resp_message}
    return jsonify(response)


@app.route('/test', methods=['POST'])
def print_dcit():
    # reference https://github.com/smokedsalmonbagel/flaskUploads/blob/main/main.py
    # https://stackoverflow.com/questions/70733510/send-blob-to-python-flask-and-then-save-it
    print("收到信息！")
    info_table = None
    try:
        info_table = request.form
        print(info_table)
    except Exception as e:
        print(e)
        print("Error at request.form")

    sr = info_table['sr']
    print("采样率：", sr)
    print("信息：", info_table["jsondata"])

    samples = None
    try:
        files = request.files
        file = files.get('file')
        print(file)
        # samples = np.frombuffer(audio_data, dtype=np.int32)
        with open("./audio/test_audio_000.wav", 'wb') as f:
            f.write(file.content)
        # print("duration：", len(samples))
    except Exception as e:
        print(e)
        print("Error at samples = np.frombuffer(info_table['audio'], dtype=np.int16)")

    # fname = "test_audio_000.wav"
    # soundfile.write(
    #     f"./audio/{fname}",
    #     samples,
    #     16000,
    #     format='WAV',
    #     subtype="FLOAT")
    # audio_file = request.files['audio']
    # # 将音频文件保存到服务器上的指定路径
    # audio_file.save('./audio/test_audio_000.wav')
    resp_message = "Data received successfully!\n"
    info_table['jsondata']['filename'] = fname
    print("filename", fname)
    response = {'message': resp_message}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
