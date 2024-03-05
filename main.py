#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:51
# @Author: ZhaoKe
# @File : main.py
# @Software: PyCharm
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("./index.html")
    # return "<p>hello world</p><br><p>ok!</p>"


# 定义上传音频文件的路由
@app.route('/getdata', methods=['POST'])
def upload():
    info_table = request.get_json()
    print(info_table)
    # audio_file = request.files['audio']
    # # 将音频文件保存到服务器上的指定路径
    # audio_file.save('./audio/test_audio_000.wav')
    response = {'message': 'Data received successfully'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
