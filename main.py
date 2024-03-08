#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/2 11:51
# @Author: ZhaoKe
# @File : main.py
# @Software: PyCharm
import os
import numpy as np
import soundfile
from flask import Flask, request, jsonify, render_template
from databasekits.table_packets import insert_use_dict

app = Flask(__name__)

CHUNK_SIZE = 1024 * 1024
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M


@app.route('/')
def index():
    return render_template("./index.html")
    # return "<p>hello world</p><br><p>ok!</p>"


total_chunks = 1024
@app.route('/merge', methods=['POST'])
def merge_chunks():
    filename = request.form.get('filename')
    chunk_dir = './recorded_audio'  # 存放分块文件的目录
    chunk_paths = [os.path.join(chunk_dir, filename + '_' + str(i)) for i in range(total_chunks)]
    try:
        with open(filename, 'wb') as f:
            for chunk_path in chunk_paths:
                with open(chunk_path, 'rb') as chunk_file:
                    f.write(chunk_file.read())
                os.remove(chunk_path)  # 删除已经合并的分块文件
        return jsonify({'code': 0, 'message': '上传成功'})
    except Exception as e:
        print(e)
        print("分块合并失败！")
        return jsonify({'code': -1, 'message': "失败："+str(e)})


@app.route('/postchunk', methods=['POST'])
def get_chunk():
    try:
        chunk = request.form.get('chunkIndex')  # 获取当前上传的块数
        filename = request.form.get('filename')  # 获取文件名
        print(f"chunk filename: {chunk}, {filename}")
        file = request.form.get('file')  # 获取上传的文件  # 这里是args不是files

        if not file or not chunk or not filename:
            return jsonify({'code': -1, 'message': '缺少参数'})

        # 创建文件夹用来存储分块
        upload_dir = './temp_files'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # 将分块保存到指定的位置
        chunk_file = os.path.join(upload_dir, filename + '.' + str(chunk))
        with open(chunk_file, 'wb') as f:
            f.write(file.read())
        print(f"保存分块:{filename}.{chunk}")
        return jsonify({'code': 0, 'message': '上传成功'})
    except Exception as e:
        print(e)
        print(f"分块上传失败！")
        return jsonify({'code': -1, 'message': str(e)})


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
    print("收到信息！")
    try:
        info_table = request.form
        print(info_table)
    except Exception as e:
        print(e)
        print("Error at request.form")
    response = {'code': 0, 'message': "table form received successfully!"}
    return jsonify(response=response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
