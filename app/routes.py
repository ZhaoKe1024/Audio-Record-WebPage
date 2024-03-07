# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-03-07 18:20
from app import app
@app.route('/')
def getIndex():
    return 'Hello Flask!'
