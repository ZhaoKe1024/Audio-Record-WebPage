# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-03-04 23:27

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'
    iditem = Column(Integer, primary_key=True)  # primary key, id
    save_name = Column(String(32))  # # 文件名，自然数
    health = Column(String(16))  # 是否健康，二值标记
    disease = Column(String(64))  # 疾病类别，自然数标记
    is_smoke = Column(String(128))  # 是否抽烟？但是儿科医院肯定不抽  # 0-1 二值
    from_device = Column(DateTime)  # 采集设备？这个其实是开集识别了  # 自然数
    from_gender = Column(String(128))  # 性别  # 0-1 二值
    from_age = Column(String(128))  # 年龄  # 二位数

    def __repr__(self):
        return "<Item(category='%s', itemname='%s', idolname='%s', performtime='%s)>" % \
               self.category, self.itemname, self.idolname, self.performtime


def insert_into_table():
    # 将数据的每一行创建为一个Item对象
    data = []
    with open("temp.csv", encoding='utf-8') as file:
        line = file.readline()
        while line:
            line_s = line.strip("\n").split(',')
            if line_s[2] == '':
                data.append(Item(category=line_s[0], itemname=line_s[1], idolname="珈乐Carol"))
            else:
                data.append(Item(category=line_s[0], itemname=line_s[1], idolname="珈乐Carol", performtime=line_s[2]))
            line = file.readline()

    # 建立连接，创建session，提交数据
    ENGINE = create_engine("mysql+pymysql://root:zksmysql@127.0.0.1:3306/asoul")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    session.add_all(data)
    session.commit()


def sqlalchemy_test():
    ENGINE = create_engine("mysql+pymysql://root:zksmysql@127.0.0.1:3306/asoul")
    # 查询2021年9月30日之后的所有item
    sql = """
        select iditem,itemname,performtime from item where performtime>'2021-9-30'
        order by performtime desc
        """
    df = pd.read_sql(sql, ENGINE)
    print(df)


if __name__ == '__main__':
    sqlalchemy_test()

