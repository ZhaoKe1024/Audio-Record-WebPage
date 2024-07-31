#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 14:30
# @Author: ZhaoKe
# @File : main_poultryinbreed.py
# @Software: PyCharm
import os.path
import time
import logging
from flask import Flask, request, jsonify, render_template, send_file

from gevent import pywsgi
from inbreed_lib.procedure.kinship_on_graph import Kinship
from inbreed_lib.BreedingMain import run_main
from inbreed_lib.func import NullNameException
from inbreed_lib.graphfromtable import get_df_from_xlsx, get_graph_from_data

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'

CHUNK_SIZE = 1024 * 1024
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20M
form_save_mode = 0  # mysql 0, local json file 1,

save_dir = "./temp_files/"


class IBCalculator(object):
    def __init__(self):
        super(IBCalculator, self).__init__()
        self.file_root = "./temp_files/"
        if os.path.exists(self.file_root):
            os.makedirs(self.file_root)
        self.analyse_template = self.file_root + "input_template.xlsx"
        self.file_to_analyze = None
        self.file_to_evaluate = None
        self.kinship = None
        self.generated_file = None
        self.keys = ["analyse", "select", "eval", "p", "p1", "help"]
        self.describe = ["分析文件并构建族谱", "生成新一年的配种方案", "评估现有方案", "计算个体近交系数",
                         "计算亲缘相关系数", "查看帮助"]

    def check_kinship(self):
        res_message = None
        if self.file_to_analyze is None:
            res_message = "请先选中待分析文件并分析。"
        if self.kinship is None:
            res_message = "请先分析文件"
        if res_message is not None:
            return {"flag": -1, "msg": res_message}
        else:
            return {"flag": 1, "msg": None}

    def analyze(self):
        if self.file_to_analyze.split(".")[-1] not in ["xlsx", "xls"]:
            raise Exception("暂时仅支持Excel文件!")
        # self.show_text_func()
        # self.kinship = Kinship(file_path=self.file_to_analyze, graph=None)
        layergraph, vertex_layer, vertex_list = get_graph_from_data(file_path=self.file_to_analyze)

        self.kinship = Kinship(graph=layergraph)

    def calc_corrcoef(self, p1: str, p2: str):
        """计算亲缘相关系数"""
        self.check_kinship()

        p1, p2 = p1.strip(), p2.strip()
        print(p1, p2)
        try:
            res = self.kinship.calc_kinship_corr(p1=p1, p2=p2)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def calc_inbrcoef(self, ct: str):
        """计算近交系数"""
        self.check_kinship()
        ct = ct.strip()
        if '.' in ct or ct == '':
            raise Exception("请输入1个自然数编号")
        try:
            res = self.kinship.calc_inbreed_coef(p=ct)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def evaluate_solution(self):
        self.check_kinship()
        sheet_list = ["16", "17", "18", "19", "20"]
        file_names = []
        for sheet_name in sheet_list[1:]:
            edges_df = get_df_from_xlsx(filepath=self.file_to_evaluate, sheet_name=sheet_name,
                                        cols=[1, 2, 3])
            with open(self.file_root + "evaluate_{}.csv".format(sheet_name), 'w', encoding="utf_8") as fout:
                fout.write("家系号,公号,母号,亲缘相关系数\n")
                for idx, row in enumerate(edges_df.itertuples()):
                    # print(row[2], row[3])
                    fout.write(f"{row[1]},{row[2]},{row[3]}," + str(
                        self.kinship.calc_kinship_corr(p1=str(row[2]), p2=str(row[3]))) + '\n')
            print(f"表格sheet{sheet_name} 评估完成！")
            file_names.append("./evaluate_{}.csv".format(sheet_name))
        return file_names


calc = IBCalculator()


def get_cur_timestr() -> str:
    return time.strftime("%Y%m%d%H%M", time.localtime())


@app.route('/')
def index():
    return render_template("./poultry_inbreedingtools.html")


@app.route('/help', methods=["GET"])
def get_help():
    ind = 0
    help_info = "家禽育种工具箱，当前支持以下功能：\n"
    ind += 1
    help_info += "(" + str(ind) + ") 文件分析（必须项）：上传一个【配种对照文件】，即历史配种信息，进行族谱初始化，然后可以基于族谱进行分析。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 谱系分析：给定一个【配种对照方案】，然后基于族谱信息分析该方案的近交程度。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 育种方案分析：输入一个目标【年份】，基于该年份以前的部分族谱，生成一个近交程度最小，或符合其他需求条件的新的配种方案。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 亲缘相关分析：给定两个同代个体的【翅号】，寻找两者的共同祖先、祖辈关系、并计算两者亲缘相关系数。\n"
    ind += 1
    help_info += "(" + str(ind) + ") 个体近交分析：给定一个个体的【翅号】，寻找其父母的共同祖先、祖辈关系、并计算两者亲缘相关系数。\n"
    # ind += 1
    # help_info += "("+str(ind)+") \n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    # help_info += "\n"
    return jsonify(response={"help": help_info})


@app.route('/download_template')
def get_template():
    if os.path.exists(calc.analyse_template):
        return send_file(calc.analyse_template, download_name=calc.analyse_template.split('/')[-1], as_attachment=True)
    else:
        raise Exception("the template file {} is not exists.".format(calc.analyse_template))


@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    # form = UploadForm()
    # if form.validate_on_submit():
    #     file = form.file.data
    #     file.save('./temp_files/' + file.filename)
    #     # 保存文件到指定路径
    #     return '文件上传成功！'
    # else:
    #     return {"flag": -1, "result": None, "msg": '文件上传失败！if form.validate_on_submit(): False!'}
    if request.method == 'POST':
        print("包含：")
        print(request.files)
        file = request.files['file_data']
        print("文件名：", file.filename)
        file.save(calc.file_root + file.filename)

        print("文件上传成功")
        calc.file_to_analyze = calc.file_root + file.filename
        calc.analyze()
        return {"flag": 0, "result": None, "msg": '文件上传成功！并且已成功分析！'}
    else:
        print("Error! method:", request.method)
        return {"flag": -1, "result": None, "msg": '错误请求类别:{}'.format(request.method)}


@app.route('/calc', methods=['GET', 'POST'])
def calculate():
    print("收到信息！")
    check = calc.check_kinship()
    if check["flag"] == -1:
        return check
    try:
        mode = None
        p, p1, p2 = -1, -1, -1
        if request.method == "POST":
            info_table = request.get_json()
            # Example
            # {"mode": "single", "Value": "7429"}
            # {"mode": "double", "Value": {"p1":"7429", p2:"7433"}}
            mode = info_table["mode"]
            if mode == "single":
                p = info_table["value"]
            elif mode == "double":
                p1 = info_table["value"]["p1"]
                p2 = info_table["value"]["p2"]
            else:
                raise Exception("Error mode, only support \'single\' or \'double\'.")

        elif request.method == "GET":
            mode = request.args.get("mode")
            if mode == "single":
                p = request.args.get("p")
            elif mode == "double":
                # 可以通过 request 的 args 属性来获取参数
                p1 = request.args.get("p1")
                p2 = request.args.get("p2")
            else:
                raise Exception("Error mode, only support \'single\' or \'double\'.")

        else:
            raise Exception("Error Unknown Method, only support \'GET\' or \'POST\'.")
        if mode == "single":
            res = calc.kinship.calc_inbreed_coef(p=p)
        elif mode == "double":
            res = calc.kinship.calc_kinship_corr(p1=p1, p2=p2)
        else:
            raise Exception("Error mode, only support \'single\' or \'double\'.")
        return jsonify(response={"res": res, "log": calc.kinship.analyzer.get_just_message()})
        # json_tosave = {}
        # for key in info_table:
        #     print(key, '\t', info_table[key])
        #     json_tosave[key] = info_table[key]
        # new_json_string = json.dumps(json_tosave, ensure_ascii=False)  # 正常显示中文
        # with open(save_dir + f"test_{info_table['filename']}.json", 'w', encoding='utf_8') as nf:
        #     nf.write(new_json_string)
        # response = {'code': 0, 'message': "table form received successfully!"}
        #
        # return jsonify(response=response)
    except Exception as e:
        print(e)
        print("Error at request.form")
        response = {'code': -1, 'message': "table form received failed" + str(e)}
        return jsonify(response=response)


@app.route('/generate')
def generate_new():
    t_year = request.args.get("t_year")
    if calc.file_to_analyze is None:
        raise Exception("The file to analyse is None.")
    calc.generated_file = None
    result_file_name = f"result_name_rand_{t_year}.csv"
    run_main(file_path=calc.file_to_analyze, gene_idx=t_year, result_file=calc.file_root+result_file_name)
    calc.generated_file = calc.file_root+result_file_name
    return jsonify({"flag": 0, "msg": "生成结果文件：{}".format(result_file_name)})


@app.route('/generate_result')
def get_generated_result():
    if calc.generated_file is None:
        raise Exception("Null File generated.")
    return send_file(calc.generated_file, download_name=calc.generated_file.split('/')[-1], as_attachment=True)


@app.route('/eval')
def eval_old():
    file_save_name = get_cur_timestr() + ".xlsx"
    if request.method == 'POST':
        file = request.files['file_data']
        print("文件名：", file.filename)
        file.save(calc.file_root + file_save_name)
        print("文件上传成功")
        calc.file_to_evaluate = calc.file_root + file_save_name
    else:
        print("Error! method:", request.method)
        return {"flag": -1, "result": None, "msg": '错误请求类别:{}'.format(request.method)}
    result_files = calc.evaluate_solution()
    res_msg = ""
    for j, iten in enumerate(result_files):
        res_msg += "("+str(j+1)+") " + iten + "\n"
    return jsonify({"flag": 0, "msg": "生成结果文件："+res_msg})


if __name__ == '__main__':
    http_server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()