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
pwd = "zkGcx_0703"


class Item(Base):
    __tablename__ = 'cough_main'
    id = Column(Integer, primary_key=True)  # primary key, id  # Even if this field is not used, it must be explicitly defined, otherwise it cannot be mapped to the data table.
    filename = Column(String(32))  # # 文件名，自然数
    # health = Column(String(16))  # 是否健康，二值标记
    disease = Column(SmallInteger())  # 疾病类别，自然数标记
    gender = Column(Boolean())  # 性别  # 0-1 二值
    age = Column(SmallInteger())  # 年龄  # 二位数
    issmoking = Column(Boolean())  # 是否抽烟？但是儿科医院肯定不抽  # 0-1 二值
    isfever = Column(Boolean())  # 是否抽烟？但是儿科医院肯定不抽  # 0-1 二值
    # from_device = Column(DateTime)  # 采集设备？这个其实是开集识别了  # 自然数

    def __repr__(self):
        return "<Item(filename='%s', disease='%s'>" % \
               self.filename, self.disease


# This function is called by the flask service
def insert_use_dict(sess_dict):
	ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/cough_schema")
	Base.metadata.create_all(ENGINE)
	Session = sessionmaker(bind=ENGINE)
	session = Session()
	try:
		fname = "null" if "filename" not in sess_dict else sess_dict['filename']
		disease_flag = -1 if "disease" not in sess_dict else sess_dict['fisease']
		session.add_all([Item(filename=fname, disease=disease_flag, gender=sess_dict['gender'], 
							age=sess_dict['age'], issmoking=sess_dict['issmoking'], isfever=sess_dict['isfever'])
						])
		session.commit()
		print("Data insert into database cough_schema table cough_main successfully!")
		sqlalchemy_test()
		return True
	except Exception as e:
		print(e)


def test_insert():
	ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/cough_schema")
	Base.metadata.create_all(ENGINE)
	Session = sessionmaker(bind=ENGINE)
	session = Session()
	try:
		session.add_all([Item(filename="test_no_pkey_0", disease=0, gender=0, age=23, issmoking=1, isfever=0)
						])
		session.commit()
		print("Data insert into database cough_schema table cough_main successfully!")
		sqlalchemy_test()
	except Exception as e:
		print(e)


def sqlalchemy_test():
    ENGINE = create_engine(f"mysql+pymysql://root:{pwd}@127.0.0.1:3306/cough_schema")
    # 查询2021年9月30日之后的所有item
    sql = """
        select * from cough_main;
        """
    df = pd.read_sql(sql, ENGINE)
    print(df)


if __name__ == '__main__':
    test_insert()
	# sqlalchemy_test()
