#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/8/1 18:06
# @Author: ZhaoKe
# @File : relationplot.py
# @Software: PyCharm
import random
from pyecharts import options as opts
from pyecharts.charts import Graph

# vertices = list(range(27))
# graph = [[10, 0], [10, 2], [12, 3], [12, 5], [18, 10], [18, 13], [13, 3], [13, 5], [19, 12], [19, 14], [14, 6], [14, 7],
#          [21, 16], [21, 17], [16, 9], [16, 12], [9, 0], [9, 1], [17, 10], [17, 11], [11, 3], [11, 4], [24, 21],
#          [24, 22], [22, 18], [22, 19], [25, 21], [25, 23], [23, 18], [23, 19]]
# depths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5]

def tuple_contrain(tList, t2):
    if len(tList) == 0:
        return False
    for item in tList:
        if item[0]==t2[0] and item[1]==t2[1]:
            return True
    return False

def generate_relation_plot(vertices_depth_edges):
    vertices = []
    # xy = []
    h_margin = 8
    for obj_item in vertices_depth_edges:
        if tuple_contrain(vertices, (obj_item[0][0], obj_item[0][1])):
            vertices.append((obj_item[0][0], obj_item[0][1]))
            # xy.append((obj_item[0][1] * h_margin))
        if tuple_contrain(vertices, (obj_item[1][0], obj_item[1][1])):
            vertices.append((obj_item[1][0], obj_item[1][1]))
            # xy.append((obj_item[1][1] * h_margin))
    print("点集:", vertices)

    xy = []

    top_m = 4
    for obj_item in vertices_depth_edges:
        xy.append([obj_item[0][1] * 8, top_m + random.randint(0, 2)])
    # vertices = [1, 2, 3, 4, 5, 6]
    # graph = [[1, 4], [2, 4], [2, 5], [3, 5], [4, 6], [5, 6]]

    # xy = [[0, 5], [0, 8], [0, 11], [2, 7], [2, 9], [4, 8]]
    # x left margin,  y: top margin
    nodes_data = []
    y_dict = dict()
    for j in range(len(vertices)):

        nodes_data.append(opts.GraphNode(x=vertices[j], y=xy[j][1], name="{}".format(vertices[j]), symbol_size=20) for j in
                  range(len(vertices)))
    links_data = []
    for item in graph:
        links_data.append(opts.GraphLink(source="{}".format(item[0]), target="{}".format(item[1]), value=2))
    c = (
        Graph()
        .add(
            "",
            nodes_data,
            links_data,
            repulsion=4000,
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{b}:{c}"
            ),
            edge_symbol=["none", "arrow"],
            layout="none"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
        )
        .render("graph_with_edge_options.html")
    )
