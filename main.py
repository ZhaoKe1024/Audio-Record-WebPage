#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:51
# @Author: ZhaoKe
# @File : main.py
# @Software: PyCharm
from flask import Flask, request

app = Flask(__name__)


# 定义上传音频文件的路由
@app.route('/index', methods=['POST'])
def upload():
    audio_file = request.files['audio']
    # 将音频文件保存到服务器上的指定路径
    audio_file.save('./audio/test_audio_000.wav')
    return '上传成功'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
