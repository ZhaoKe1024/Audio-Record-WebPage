#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/30 15:08
# @Author: ZhaoKe
# @File : inbreed_accounts.py
# @Software: PyCharm
import json
import pandas as pd
from sqlalchemy import create_engine, select, Column, text as sql_text
from sqlalchemy import Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

# json_str = None  # json string
with open("./accounts.json", 'r', encoding='utf_8') as fp:
    json_str = fp.read()
json_data = json.loads(json_str)  # get json from json string
pwd = json_data["202407"]  # Reborn_240729
print(pwd)  # <class 'dict'>


class accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer,
                primary_key=True)  # primary key, id  # Even if this field is not used, it must be explicitly defined, otherwise it cannot be mapped to the data table.
    username = Column(String(16))  # # 文件名，自然数
    password = Column(String(16))  # 是否健康，二值标记

    # from_device = Column(DateTime)  # 采集设备？这个其实是开集识别了  # 自然数

    def __repr__(self):
        return "<Item(username='%s', password='%s'>" % (self.filename, "******")


def test_insert():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/inbreed")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        session.add_all([Item(filename="test_no_pkey_1", disease="healthy", gender='0', age='19', issmoking='0', isfever='1')
                         ])
        session.commit()
        print("????????????????????????????????????????")
        print("Data insert into database cough_schema table cough_main successfully!")
        sqlalchemy_test()
    except Exception as e:
        print(e)


def sqlalchemy_test():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/inbreed")
    # 查询2021年9月30日之后的所有item
    sql = "select * from accounts;"
    df = pd.read_sql_query(con=ENGINE.connect(), sql=sql_text(sql))
    print(df.iloc[:, :2])


def sqlalchemy_test1():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/inbreed")
    Base.metadata.create_all(ENGINE)
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    try:
        session.execute(select(accounts))
        print("Data insert into database cough_schema table cough_main successfully!")
        sqlalchemy_test()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    sqlalchemy_test()
